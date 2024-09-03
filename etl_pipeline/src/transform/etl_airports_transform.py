import sys
sys.path.append('/opt/bitnami/spark/jobs')

from pyspark.sql import SparkSession

from src.utils.etl_transform import EtlTransform
from src.utils.schema import aiports_schema


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlAirportTransform") \
        .getOrCreate()

    etl_flights = EtlTransform(spark, input_path, output_path, aiports_schema)
    etl_flights.run()


if __name__ == "__main__":
    main()
