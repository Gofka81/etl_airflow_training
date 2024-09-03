import sys
sys.path.append('/opt/bitnami/spark/jobs')

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from src.utils.etl_transform import EtlTransform
from src.utils.schema import airlines_schema


class EtlAirlinesTransform(EtlTransform):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str, schema):
        super().__init__(spark, input_path, output_path, schema)

    @staticmethod
    def transform(df: DataFrame) -> DataFrame:
        transformed_df = df.withColumn("name", col("Name"))\
                            .withColumn("code", col("Code"))\
                            .withColumn("icao", col("ICAO"))
        return transformed_df


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlAirlinesTransform") \
        .getOrCreate()

    etl_flights = EtlAirlinesTransform(spark, input_path, output_path, airlines_schema)
    etl_flights.run()


if __name__ == "__main__":
    main()
