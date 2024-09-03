from keras_spark.core import SparkDsTFDs, KerasOnSparkPredict
import tensorflow as tf
from pyspark.sql import DataFrame as SparkDataFrame
from typing import Any, Dict


class KerasSparkModel(tf.keras.Model):
    """
    A custom Keras model that extends the TensorFlow Keras Model to work with Apache Spark DataFrames.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the KerasSparkModel.

        :param args: Positional arguments for the base Keras Model.
        :param kwargs: Keyword arguments for the base Keras Model.
        """
        super(KerasSparkModel, self).__init__(*args, **kwargs)

    def fit(
        self,
        x: Any,
        y: Any = None,
        partition_col: str = "partition_id",
        partition_values: int = range(1),
        num_parallel_calls: int = 1,
        **kwargs: Dict[str, Any]
    ) -> None:
        """
        Fit the model to the data. If the data is a Spark DataFrame, convert it to a TensorFlow dataset before fitting.

        :param x: Input data. Must be a Spark DataFrame or other acceptable type for Keras models.
        :param y: Target data. Not used if x is a Spark DataFrame.
        :param partition_col: Column name used for partitioning the Spark DataFrame.
        :param nr_partitions: Number of partitions for the Spark DataFrame.
        :param num_parallel_calls: Number of parallel calls for data processing.
        :param kwargs: Additional arguments passed to the `fit` method of the Keras Model.
        """
        if isinstance(x, SparkDataFrame):
            # Convert Spark DataFrame to TensorFlow dataset using SparkDsTFDs adapter
            adapter = SparkDsTFDs(self)
            dataset = adapter.convert(
                x,
                partition_col=partition_col,
                partition_values=partition_values,
                num_parallel_calls=num_parallel_calls,
                batch_size=kwargs['batch_size']
            )
            # Call the base class fit method with the converted dataset
            super(KerasSparkModel, self).fit(dataset, **kwargs)
        else:
            # Call the base class fit method directly if x is not a Spark DataFrame
            super(KerasSparkModel, self).fit(x, y, **kwargs)

    def predict(self, x: Any,**kwargs: Dict[str, Any]) -> Any:
        """
        Make predictions using the model. If the input is a Spark DataFrame, use Spark for distributed prediction.

        :param x: Input data for prediction. Must be a Spark DataFrame or other acceptable type for Keras models.
        :param kwargs: Additional arguments passed to the `predict` method of the Keras Model.
        :return: Predictions made by the model.
        """
        if isinstance(x, SparkDataFrame):
            # Use KerasOnSparkPredict to make predictions on Spark DataFrame
            return KerasOnSparkPredict().predict(x, self)
        else:
            # Call the base class predict method directly if x is not a Spark DataFrame
            return super(KerasSparkModel, self).predict(x, **kwargs)
