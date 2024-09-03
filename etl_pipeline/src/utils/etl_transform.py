from abc import ABC, abstractmethod
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType


class EtlTransform(ABC):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str, schema: StructType):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path
        self.schema = schema

    def run(self):
        extracted_df = self.extract()
        transformed_df = self.transform(extracted_df)
        self.load(transformed_df)

    def extract(self) -> DataFrame:
        return self.spark.read.json(self.input_path, multiLine=True, schema=self.schema)

    @staticmethod
    def transform(df: DataFrame) -> DataFrame:
        return df

    def load(self, final_df: DataFrame):
        final_df.write.parquet(self.output_path)
