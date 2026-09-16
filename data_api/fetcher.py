import requests
from datetime import datetime

from data_api.cache import save_to_cache, load_from_cache


def fetch_weather(latitude, longitude):
    """
    Fetch Antarctic weather data from Open-Meteo.
    Uses local cache if API is unavailable.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
        "forecast_days": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            raise requests.RequestException(
                f"HTTP {response.status_code}"
            )

        result = response.json()

        if "hourly" not in result:
            raise ValueError(
                "Invalid response format"
            )

        live_data = {
            "source": "Open-Meteo",
            "last_updated": datetime.utcnow().isoformat(),
            "data_status": "LIVE",
            "data": result["hourly"]
        }

        # Save successful API response locally
        save_to_cache(live_data)

        return live_data

    except (requests.RequestException, ValueError):

        # API unavailable → use local cache
        cached_data = load_from_cache()

        if cached_data is not None:
            return {
                "source": "local_cache",
                "last_updated": cached_data.get(
                    "last_updated"
                ),
                "data_status": "CACHED",
                "data": cached_data.get("data")
            }

        # No API and no cache
        return {
            "source": "local_cache",
            "last_updated": None,
            "data_status": "UNAVAILABLE",
            "data": None,
            "error": "API unavailable and no cache found"
        }