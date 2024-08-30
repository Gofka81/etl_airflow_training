import sys
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col
from pyspark.sql.types import StructField, IntegerType, StringType, FloatType, StructType

from etl_pipeline.utils.etl_transform import EtlTransform


class EtlAirlinesTransform(EtlTransform):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        super().__init__(spark, input_path, output_path)

    def extract(self) -> DataFrame:
        schema = StructType([
            StructField("Name", StringType(), True),
            StructField("Code", StringType(), True),
            StructField("ICAO", StringType(), True)
        ])
        return self.spark.read.json(self.input_path, multiLine=True, schema=schema)

    def transform(self, df: DataFrame) -> DataFrame:
        transformed_df = df.withColumn("name", col("Name"))\
                            .withColumn("code", col("Code"))\
                            .withColumn("icao", col("ICAO"))
        transformed_df.show()
        return transformed_df


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlAirlinesTransform") \
        .getOrCreate()

    etl_flights = EtlAirlinesTransform(spark, input_path, output_path)
    etl_flights.run()


if __name__ == "__main__":
    main()
