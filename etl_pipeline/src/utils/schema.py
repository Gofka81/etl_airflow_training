from pyspark.sql.types import StructField, IntegerType, StringType, FloatType, StructType

aiports_schema = StructType([
    StructField("latitude", FloatType(), nullable=True),
    StructField("longitude", FloatType(), nullable=True),
    StructField("altitude", IntegerType(), nullable=True),
    StructField("name", StringType(), nullable=True),
    StructField("icao", StringType(), nullable=True),
    StructField("iata", StringType(), nullable=False),
    StructField("country", StringType(), nullable=True)
])


airlines_schema = StructType([
    StructField("Name", StringType(), True),
    StructField("Code", StringType(), True),
    StructField("ICAO", StringType(), True)
])

flights_schema = StructType([
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