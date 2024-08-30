from abc import ABC, abstractmethod
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


class EtlTransform(ABC):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        extracted_df = self.extract()
        transformed_df = self.transform(extracted_df)
        self.load(transformed_df)

    @abstractmethod
    def extract(self) -> DataFrame:
        pass

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        pass

    def load(self, final_df: DataFrame):
        final_df.write.parquet(self.output_path)
