import sys
sys.path.append('/opt/bitnami/spark/jobs')
import datetime

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col, lit, unix_timestamp

from etl_pipeline.src.utils.etl_transform import EtlTransform
from etl_pipeline.src.utils.schema import flights_schema


class EtlFlightsTransform(EtlTransform):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str, execution_date: str, schema):
        super().__init__(spark, input_path, output_path, schema)
        self.execution_date = execution_date

    def transform(self, df: DataFrame) -> DataFrame:
        new_df = df.withColumn('timestamp', unix_timestamp(lit(self.execution_date))).drop('time')
        new_df.show()
        return new_df


def main():
    input_path = '/Users/lantonyk/Developer/DataEng/POC project/etl_airflow_training/flights.json'
    output_path = 'test-result'
    execution_date = '2024-09-09 16:28:09'
    print(execution_date)

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlFlightsTransform") \
        .getOrCreate()

    etl_flights = EtlFlightsTransform(spark, input_path, output_path, execution_date, flights_schema)
    etl_flights.run()


if __name__ == "__main__":
    main()
