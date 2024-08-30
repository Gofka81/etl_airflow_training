import sys
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col
from pyspark.sql.types import StructField, IntegerType, StringType, FloatType, StructType


class EtlFlightsTransform:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        extracted_df = self.extract()
        transformed_df = self.transform(extracted_df)
        self.load(transformed_df)

    def extract(self) -> DataFrame:
        schema = StructType([
            StructField("latitude", FloatType(), True),
            StructField("longitude", FloatType(), True),
            StructField("id", StringType(), False),
            StructField("icao_24bit", StringType(), True),
            StructField("heading", IntegerType(), True),
            StructField("altitude", IntegerType(), True),
            StructField("ground_speed", IntegerType(), True),
            StructField("squawk", StringType(), True),
            StructField("aircraft_code", StringType(), True),
            StructField("registration", StringType(), True),
            StructField("time", FloatType(), True),
            StructField("origin_airport_iata", StringType(), True),
            StructField("destination_airport_iata", StringType(), True),
            StructField("number", StringType(), True),
            StructField("airline_iata", StringType(), True),
            StructField("on_ground", IntegerType(), True),
            StructField("vertical_speed", IntegerType(), True),
            StructField("callsign", StringType(), True),
            StructField("airline_icao", StringType(), True),
        ])
        return self.spark.read.json(self.input_path, multiLine=True, schema=schema)

    def transform(self, df: DataFrame) -> DataFrame:
        df.show()
        return df

    def load(self, final_df: DataFrame):
        final_df.write.parquet(self.output_path)


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlFlightsTransform") \
        .getOrCreate()

    etl_flights = EtlFlightsTransform(spark, input_path, output_path)
    etl_flights.run()


if __name__ == "__main__":
    main()
