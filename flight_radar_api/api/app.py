from fastapi import FastAPI, HTTPException
from FlightRadar24 import FlightRadar24API

from ..utils.flight_utils import get_region_bounds

app = FastAPI()
flightradar_api: FlightRadar24API = FlightRadar24API()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FlightRadar24 API Microservice"}


@app.get("/flights")
def get_flights():
    try:
        region_list = get_region_bounds(flightradar_api)

        res = []

        for region_bound, region_name in region_list:
            flights = flightradar_api.get_flights(bounds=flightradar_api.get_bounds(region_bound))
            res += flights

        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/flights/{airline_code}")
def get_flights_by_airline(airline_code: str):
    try:
        flights = flightradar_api.get_flights(airline=airline_code, details=True)
        return flights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/flight/{flight_id}")
def get_flight_details(flight_id: str):
    try:
        flight = flightradar_api.get_flight_details(flight_id)
        if flight:
            return flight
        else:
            raise HTTPException(status_code=404, detail="Flight not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/airports")
def get_airports():
    try:
        airports = flightradar_api.get_airports()
        return airports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/airlines")
def get_airlines():
    try:
        airlines = flightradar_api.get_airlines()
        return airlines
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
