# =========================================================
# ANTARCTIC AI - M5 DATA ADAPTER
# M5 - Khushi
# Connects M3 data with M4/M5 modules
# =========================================================

from data_api.fetcher import fetch_weather
from iceberg.loader import (
    load_antarctic_icebergs,
    prepare_iceberg_data,
    get_nearby_icebergs_with_distance
)

ICEBERG_FILE = "data/AntarcticIcebergs_20260910.csv"


def get_navigation_data(latitude, longitude):
    """
    Collect available real M3 data for M5 risk and route analysis.
    """

    result = {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "weather": None,
        "iceberg": None,
        "sea_ice": {
            "data_status": "UNAVAILABLE",
            "concentration": None
        }
    }

    # -----------------------------------------------------
    # WEATHER DATA
    # -----------------------------------------------------
    weather = fetch_weather(latitude, longitude)

    if weather.get("data"):
        data = weather["data"]

        result["weather"] = {
            "source": weather.get("source"),
            "data_status": weather.get("data_status"),
            "wind_speed": data.get("wind_speed_10m", [None])[0],
            "temperature": data.get("temperature_2m", [None])[0],
            "precipitation": data.get("precipitation", [None])[0]
        }

    # -----------------------------------------------------
    # ICEBERG DATA
    # -----------------------------------------------------
    iceberg_data = load_antarctic_icebergs(ICEBERG_FILE)
    iceberg_data = prepare_iceberg_data(iceberg_data)

    nearby = get_nearby_icebergs_with_distance(
        iceberg_data,
        latitude,
        longitude,
        max_distance_km=1000
    )

    if nearby:
        nearest = min(
            nearby,
            key=lambda iceberg: iceberg["distance_km"]
        )

        result["iceberg"] = {
            "count": len(nearby),
            "nearest_distance_km": nearest["distance_km"],
            "nearest_iceberg": nearest
        }
    else:
        result["iceberg"] = {
            "count": 0,
            "nearest_distance_km": None,
            "nearest_iceberg": None
        }

    return result