from dataclasses import dataclass

@dataclass
class AirportDTO:
    icao: str           # ICAO code (e.g., "EGLL" for London Heathrow)
    iata: str           # IATA code (e.g., "LHR" for London Heathrow)
    name: str           # Full name of the airport
    city: str           # City where the airport is located
    country: str        # Country where the airport is located
    latitude: float     # Latitude of the airport
    longitude: float    # Longitude of the airport
    timezone: str       # Timezone of the airport (e.g., "Europe/London")
    elevation: int      # Elevation in feet
    type: str           # Type of airport (e.g., "large_airport", "small_airport")
    website: str        # Official website of the airport (optional)
    runways: int        # Number of runways
    terminal_count: int # Number of terminals (optional)

