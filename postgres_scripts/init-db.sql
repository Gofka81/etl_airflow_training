-- Create the database
CREATE DATABASE etl_training;

-- Connect to the newly created database
\c etl_training

-- Create airline_info table
CREATE TABLE airline_info (
                              Name VARCHAR(255),
                              Code VARCHAR(50),
                              ICAO VARCHAR(10) PRIMARY KEY
);

-- Create airport_info table
CREATE TABLE airport_info (
                              latitude DOUBLE PRECISION,
                              longitude DOUBLE PRECISION,
                              altitude INTEGER,
                              name VARCHAR(255),
                              icao VARCHAR(10),
                              iata VARCHAR(10) PRIMARY KEY,
                              country VARCHAR(100)
);

-- Create flight_data table
CREATE TABLE flight_data (
                             latitude DOUBLE PRECISION,
                             longitude DOUBLE PRECISION,
                             id VARCHAR(50) PRIMARY KEY,
                             icao_24bit VARCHAR(10),
                             heading INTEGER,
                             altitude INTEGER,
                             ground_speed INTEGER,
                             squawk VARCHAR(10),
                             aircraft_code VARCHAR(10),
                             registration VARCHAR(20),
                             time BIGINT,
                             origin_airport_iata VARCHAR(5),
                             destination_airport_iata VARCHAR(5),
                             number VARCHAR(20),
                             airline_iata VARCHAR(5),
                             on_ground INTEGER,
                             vertical_speed INTEGER,
                             callsign VARCHAR(10),
                             airline_icao VARCHAR(4)
);
