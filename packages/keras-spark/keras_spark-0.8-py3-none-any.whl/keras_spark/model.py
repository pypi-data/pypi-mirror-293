from core import SparkDsTFDs,KerasOnSparkPredict
import tensorflow as tf
from pyspark.sql import DataFrame as SparkDataFrame

class SparkKerasModel(tf.keras.Model):

    def __init__(self, *args, **kwargs):
        super(SparkKerasModel, self).__init__(*args, **kwargs)

    def fit(self, x=None, y=None, partition_col="batch_id",nr_partitions=100,num_parallel_calls=1, **kwargs):

        if isinstance(x, SparkDataFrame):

            adapter = SparkDsTFDs(self)
            dataset = adapter.convert(x, partition_col=partition_col, nr_partitions=nr_partitions, num_parallel_calls=num_parallel_calls, batch_size=kwargs['batch_size'])

            super(SparkKerasModel, self).fit(dataset,**kwargs)

        else:
            super(SparkKerasModel, self).fit(x, y, **kwargs)

    def predict(self, x=None, **kwargs):

        if isinstance(x, SparkDataFrame):

            return KerasOnSparkPredict().predict(x,self)

        else:
            return super(SparkKerasModel, self).predict(x, **kwargs)
