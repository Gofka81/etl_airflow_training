import sys
sys.path.append('/opt/bitnami/spark/jobs')

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import explode, col, lit

from src.utils.etl_transform import EtlTransform
from src.utils.schema import flights_schema


class EtlFlightsTransform(EtlTransform):
    def __init__(self, spark: SparkSession, input_path: str, output_path: str, execution_date: str, schema):
        super().__init__(spark, input_path, output_path, schema)
        self.execution_date = execution_date

    def transform(self, df: DataFrame) -> DataFrame:
        df.show()
        new_df = (df.withColumn('timestamp', lit(self.execution_date))
                  .select("timestamp", "latitude", "longitude", "id", "icao_24bit", "heading", "altitude",
                          "ground_speed", "squawk", "aircraft_code", "registration", "origin_airport_iata",
                          "destination_airport_iata", "number", "airline_iata", "on_ground", "vertical_speed",
                          "callsign", "airline_icao")
                  )
        return new_df


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    execution_date = sys.argv[3]

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("EtlFlightsTransform") \
        .getOrCreate()

    etl_flights = EtlFlightsTransform(spark, input_path, output_path, execution_date, flights_schema)
    etl_flights.run()


if __name__ == "__main__":
    main()
