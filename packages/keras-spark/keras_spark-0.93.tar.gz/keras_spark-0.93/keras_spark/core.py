import tensorflow as tf
from pyspark.sql import functions as F
from collections.abc import Iterator
from pyspark.sql import SparkSession
import tempfile
import pandas as pd
from pyspark.sql.types import StructType, StructField, ArrayType, IntegerType, FloatType, StringType, DoubleType


class SparkDsTFDs():

    def __init__(self,model):

        def unify_input(keras_input):
            if type(keras_input) == list:
                return keras_input
            elif type(keras_input) == dict:
                return keras_input.values()
            else:
                return [keras_input]

        self.model = model
        self.input_names =  [layer.name for layer in unify_input(self.model.input)]
        self.output_names = list(self.model.output_names)
        self.shape_dict,self.type_dict = self.get_dicts()

    def get_dicts(self):
        shape_dict={}
        type_dict={}
        for name in self.input_names:
            shape_dict[name] = self.model.get_layer(name)._input_tensor.shape[1:]
            type_dict[name] = self.model.get_layer(name).dtype
        for name in self.output_names:
            shape_dict[name] = self.model.get_layer(name).output.shape[1:]
            type_dict[name] = self.model.get_layer(name).output.dtype
        return (shape_dict,type_dict)


    def pandas_to_tensor_dict(self, pandas_df, as_dict=False, only_inputs=False):
        op = {}
        input_names = self.input_names
        output_names = self.output_names
        if only_inputs:
            output_names=[]

        def extract_tensor(column_name):
            tensor = tf.constant(pandas_df[column_name].values.tolist())
            reshaped = tf.reshape(tensor, [-1] + list(self.shape_dict[name]))  # Preserve batch size
            return  tf.cast(reshaped, self.type_dict[name])

        for name in input_names+output_names:
            assert name in pandas_df.columns,f"column {name} isn't contained in dataset"
            op[name] = extract_tensor(name)

        if as_dict:
            return op
        else:
            return tuple([op[name] for name in input_names + output_names])

    def convert(self,spark_df,partition_col,nr_partitions,batch_size,num_parallel_calls=None):

        def _get_tensors_from_partition(partition_id):
            pdf = spark_df.filter(F.col(partition_col) == F.lit(int(partition_id))).toPandas()
            return self.pandas_to_tensor_dict(pdf)

        get_tensors_from_partition = lambda i: tf.py_function(
            _get_tensors_from_partition,
            [i],
            Tout=[tf.TensorSpec(shape=self.shape_dict[name], dtype=self.type_dict[name]) for name in
                  self.input_names + self.output_names]
        )

        dataset = (
            tf.data.Dataset.range(nr_partitions)
            .interleave(
                lambda id: tf.data.Dataset.from_tensor_slices(tuple(get_tensors_from_partition(id)))
                .map(lambda *flist: ({n: flist[i] for i, n in enumerate(self.input_names)},
                                     {n: flist[len(self.input_names) + i] for i, n in enumerate(self.output_names)}
                                     )
                     )
                .map(lambda x, y: ({k: tf.reshape(v, self.shape_dict[k]) for k, v in x.items()},
                                   {k: tf.reshape(v, self.shape_dict[k]) for k, v in y.items()}
                                   )
                     )
                , num_parallel_calls= (num_parallel_calls or tf.data.AUTOTUNE)
            )
            .map(lambda x, y: (x, (y[list(y.keys())[0]]) if len(y) == 1 else y))
            .batch(batch_size)
            .prefetch(tf.data.AUTOTUNE)
        )

        return dataset

class KerasOnSparkPredict:

    def infer_output_schema_from_keras(self,model):

        def map_keras_dtype_to_spark(dtype):
            """Maps Keras output data types to corresponding Spark data types."""
            if dtype == tf.int32:
                return IntegerType()
            elif dtype == tf.float32:
                return FloatType()
            elif dtype == tf.float64:
                return DoubleType()
            elif dtype == tf.string:
                return StringType()
            else:
                raise ValueError(f"Unsupported dtype: {dtype}")

        output_dict = model.output
        schema_fields = []

        for key, tensor in output_dict.items():
            spark_type = map_keras_dtype_to_spark(tensor.dtype)
            if len(tensor.shape) > 1:
                for _ in range(1,len(tensor.shape)):
                    spark_type = ArrayType(spark_type)
            schema_fields.append(StructField(key, spark_type, nullable=False))

        schema = StructType(schema_fields)
        type_string = f"struct<{','.join([f'{field.name}: {field.dataType.simpleString()}' for field in schema.fields])}>"

        return type_string


    def keras_output_to_dict(self,model):

        output_names = self.model.output_names

        if type(model.output) == dict:
            return model
        elif type(model.output) == list:
            return tf.keras.models.Model(model.input,{o._keras_history.operation.name:o for o in zip(model.output,output_names)})

        elif tf.keras.backend.is_keras_tensor(model.output):
            return tf.keras.models.Model(model.input, {o._keras_history.operation.name: o for o in [model.output]})
        else:
            raise Exception("this keras model has an unknown output type ")

    def predict(self, spark_df, model, use_spark_files=True,local_path = "/users/csommeregger",maxRecordsPerBatch=100):

        model = self.keras_output_to_dict(model)
        spark = SparkSession.builder.getOrCreate()
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
        spark.conf.set('spark.sql.execution.arrow.maxRecordsPerBatch', maxRecordsPerBatch)

        temp_file_name=next(tempfile._get_candidate_names())
        mpath = f"{local_path}/{temp_file_name}.keras"
        model.save(mpath)

        if use_spark_files:
            spark.sparkContext.addFile(mpath,recursive=True)
        else:
            mweights = model.get_weights()
            mjson = model.to_json()

        def raw_predict(iterator: Iterator[pd.DataFrame]) -> Iterator[pd.DataFrame]:

            from keras.src.saving import serialization_lib
            serialization_lib.enable_unsafe_deserialization()

            if use_spark_files:
                model = tf.keras.models.load_model(mpath, custom_objects={'tf': tf})
            else:
                model = tf.keras.models.model_from_json(mjson, custom_objects={'tf': tf})
                model.set_weights(mweights)

            spa = SparkDsTFDs(model)

            for pdf_full in iterator:
                td = spa.pandas_to_tensor_dict(pdf_full,as_dict=True,only_inputs=True)
                dict_output = model(td)
                yield pd.DataFrame({k:v.numpy().tolist() for k,v in dict_output.items()})

        type_str = self.infer_output_schema_from_keras(model)
        col_struct = F.struct(*spark_df.columns)
        op =  spark_df.withColumn("model_output", F.pandas_udf(type_str)(raw_predict)(col_struct)).cache()
        return op