import json
from datetime import datetime, timezone
from pathlib import Path

import requests


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

CACHE_DIR = ROOT / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"

REQUEST_TIMEOUT = 15

# Cached data older than this is considered STALE.
STALE_AFTER_SECONDS = 24 * 60 * 60


# ============================================================
# COMMON HELPERS
# ============================================================

def _now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def _iso(dt):
    """Convert datetime to ISO string."""
    if dt is None:
        return None

    if isinstance(dt, datetime):
        return dt.isoformat()

    return str(dt)


def _valid_coordinates(latitude, longitude):
    """Validate latitude and longitude."""
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return False

    return (
        -90 <= latitude <= 90
        and -180 <= longitude <= 180
    )


def _cache_path(name):
    """Return cache file path."""
    return CACHE_DIR / f"{name}.json"


def _save_cache(name, result):
    """Save successful real API result to cache."""
    try:
        payload = {
            "cached_at": _now().isoformat(),
            "result": result,
        }

        with open(
            _cache_path(name),
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                payload,
                file,
                indent=2,
                ensure_ascii=False
            )

    except Exception:
        # Cache failure must never crash the application.
        pass


def _load_cache(name):
    """Load cached result."""
    path = _cache_path(name)

    if not path.exists():
        return None

    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception:
        return None


def _fallback(name, error):
    """
    Return previous real cached data.

    Cached data:
        recent -> FALLBACK
        old    -> STALE

    No fake values are generated.
    """

    cached = _load_cache(name)

    if not cached:
        return {
            "status": "UNAVAILABLE",
            "source": None,
            "last_updated": None,
            "data": None,
            "error": str(error),
        }

    result = cached.get("result")

    if not isinstance(result, dict):
        return {
            "status": "UNAVAILABLE",
            "source": None,
            "last_updated": None,
            "data": None,
            "error": str(error),
        }

    cached_at_text = cached.get("cached_at")

    try:
        cached_at = datetime.fromisoformat(
            cached_at_text
        )

        if cached_at.tzinfo is None:
            cached_at = cached_at.replace(
                tzinfo=timezone.utc
            )

        age_seconds = (
            _now() - cached_at
        ).total_seconds()

    except Exception:
        age_seconds = STALE_AFTER_SECONDS + 1

    if age_seconds <= STALE_AFTER_SECONDS:
        status = "FALLBACK"
    else:
        status = "STALE"

    return {
        "status": status,
        "source": result.get("source"),
        "last_updated": result.get("last_updated"),
        "data": result.get("data"),
        "error": str(error),
    }


# ============================================================
# WEATHER
# ============================================================

def fetch_weather(latitude, longitude):
    """
    Fetch current weather from Open-Meteo.

    Returns:
    {
        status,
        source,
        last_updated,
        data,
        error
    }
    """

    if not _valid_coordinates(
        latitude,
        longitude
    ):
        return {
            "status": "UNAVAILABLE",
            "source": "Open-Meteo Weather API",
            "last_updated": None,
            "data": None,
            "error": "Invalid latitude or longitude.",
        }

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "surface_pressure,"
            "visibility,"
            "wind_speed_10m,"
            "wind_direction_10m,"
            "wind_gusts_10m"
        ),
        "wind_speed_unit": "kmh",
        "temperature_unit": "celsius",
        "timezone": "GMT",
    }

    try:
        response = requests.get(
            WEATHER_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        payload = response.json()

        current = payload.get("current", {})

        result = {
            "status": "LIVE",
            "source": "Open-Meteo Weather API",
            "last_updated": current.get("time"),
            "data": {
                "temperature_c": current.get(
                    "temperature_2m"
                ),
                "relative_humidity_percent": current.get(
                    "relative_humidity_2m"
                ),
                "pressure_hpa": current.get(
                    "surface_pressure"
                ),
                "visibility_m": current.get(
                    "visibility"
                ),
                "wind_speed_kmh": current.get(
                    "wind_speed_10m"
                ),
                "wind_direction_deg": current.get(
                    "wind_direction_10m"
                ),
                "wind_gust_kmh": current.get(
                    "wind_gusts_10m"
                ),
            },
            "error": None,
        }

        _save_cache(
            "weather",
            result
        )

        return result

    except Exception as error:
        return _fallback(
            "weather",
            error
        )


# ============================================================
# MARINE / OCEAN
# ============================================================

def fetch_marine(latitude, longitude):
    """
    Fetch current marine/ocean information
    from Open-Meteo Marine API.
    """

    if not _valid_coordinates(
        latitude,
        longitude
    ):
        return {
            "status": "UNAVAILABLE",
            "source": "Open-Meteo Marine API",
            "last_updated": None,
            "data": None,
            "error": "Invalid latitude or longitude.",
        }

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "wave_height,"
            "wave_direction,"
            "wave_period,"
            "sea_surface_temperature,"
            "ocean_current_velocity,"
            "ocean_current_direction"
        ),
        "timezone": "GMT",
    }

    try:
        response = requests.get(
            MARINE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        payload = response.json()

        current = payload.get(
            "current",
            {}
        )

        result = {
            "status": "LIVE",
            "source": "Open-Meteo Marine API",
            "last_updated": current.get(
                "time"
            ),
            "data": {
                "wave_height_m": current.get(
                    "wave_height"
                ),
                "wave_direction_deg": current.get(
                    "wave_direction"
                ),
                "wave_period_s": current.get(
                    "wave_period"
                ),
                "sea_surface_temperature_c": current.get(
                    "sea_surface_temperature"
                ),
                "ocean_current_velocity_kmh": current.get(
                    "ocean_current_velocity"
                ),
                "ocean_current_direction_deg": current.get(
                    "ocean_current_direction"
                ),
            },
            "error": None,
        }

        _save_cache(
            "marine",
            result
        )

        return result

    except Exception as error:
        return _fallback(
            "marine",
            error
        )


# ============================================================
# SEA ICE
# ============================================================

def fetch_sea_ice(
    latitude,
    longitude,
    data_date=None
):
    """
    Fetch Antarctic sea-ice concentration
    using the existing NOAA/NSIDC integration.

    Existing data_api.py is preserved.
    """

    if not _valid_coordinates(
        latitude,
        longitude
    ):
        return {
            "status": "UNAVAILABLE",
            "source": "NOAA/NSIDC",
            "last_updated": None,
            "data": None,
            "error": "Invalid latitude or longitude.",
        }

    try:
        from sea_ice_api.sea_ice import (
            fetch_sea_ice as existing_fetch
        )

        result = existing_fetch(
            latitude,
            longitude,
            data_date
        )

        if not isinstance(result, dict):
            return {
                "status": "UNAVAILABLE",
                "source": "NOAA/NSIDC",
                "last_updated": None,
                "data": None,
                "error": "Invalid sea-ice response.",
            }

        old_status = result.get(
            "data_status"
        )

        if old_status == "LIVE":
            status = "LIVE"

        elif old_status == "UNAVAILABLE":
            status = "UNAVAILABLE"

        else:
            status = "STALE"

        return {
            "status": status,
            "source": "NOAA/NSIDC",
            "last_updated": result.get(
                "last_updated"
            ),
            "data": result.get(
                "data"
            ),
            "error": result.get(
                "error"
            ),
        }

    except Exception as error:
        return {
            "status": "UNAVAILABLE",
            "source": "NOAA/NSIDC",
            "last_updated": None,
            "data": None,
            "error": str(error),
        }


# ============================================================
# ICEBERG
# ============================================================

def _find_latest_iceberg_csv():
    """
    Find latest Antarctic iceberg CSV
    from existing data directory.
    """

    data_dir = ROOT / "data"

    files = list(
        data_dir.glob(
            "AntarcticIcebergs_*.csv"
        )
    )

    if not files:
        return None

    return max(
        files,
        key=lambda path: path.stat().st_mtime
    )


def _get_iceberg_last_updated(icebergs):
    """
    Extract last update safely from either
    DataFrame or list structure.
    """

    if icebergs is None:
        return None

    # Pandas DataFrame
    try:
        if hasattr(icebergs, "empty"):

            if icebergs.empty:
                return None

            if "Last Update" in icebergs.columns:
                return str(
                    icebergs.iloc[0]["Last Update"]
                )

            if "last_update" in icebergs.columns:
                return str(
                    icebergs.iloc[0]["last_update"]
                )

            return None

    except Exception:
        pass

    # List of dictionaries
    if isinstance(icebergs, list):

        if not icebergs:
            return None

        first = icebergs[0]

        if isinstance(first, dict):
            return first.get(
                "last_update"
            )

    return None


def _iceberg_count(icebergs):
    """Safely get iceberg count."""

    if icebergs is None:
        return 0

    try:
        if hasattr(icebergs, "empty"):
            return len(icebergs)
    except Exception:
        pass

    try:
        return len(icebergs)
    except Exception:
        return 0


def fetch_icebergs(
    latitude=None,
    longitude=None,
    max_distance_km=None
):
    """
    Load official USNIC Antarctic iceberg dataset.

    If latitude/longitude are supplied:
        return nearby icebergs.

    If coordinates are not supplied:
        return all prepared icebergs.
    """

    try:
        from iceberg.loader import (
            load_antarctic_icebergs,
            get_nearby_icebergs_with_distance
        )

        csv_path = _find_latest_iceberg_csv()

        if csv_path is None:
            return {
                "status": "UNAVAILABLE",
                "source": (
                    "USNIC Antarctic Iceberg Dataset"
                ),
                "last_updated": None,
                "data": None,
                "error": (
                    "Antarctic iceberg CSV not found."
                ),
            }

        icebergs = load_antarctic_icebergs(
            csv_path
        )

        if icebergs is None:
            return {
                "status": "UNAVAILABLE",
                "source": (
                    "USNIC Antarctic Iceberg Dataset"
                ),
                "last_updated": None,
                "data": None,
                "error": (
                    "Iceberg dataset could not be loaded."
                ),
            }

        last_updated = _get_iceberg_last_updated(
            icebergs
        )

        # ----------------------------------------------------
        # Nearby iceberg search
        # ----------------------------------------------------

        if (
            latitude is not None
            and longitude is not None
        ):

            if max_distance_km is None:
                max_distance_km = 100

            try:
                max_distance_km = float(
                    max_distance_km
                )
            except (
                TypeError,
                ValueError
            ):
                return {
                    "status": "UNAVAILABLE",
                    "source": (
                        "USNIC Antarctic Iceberg Dataset"
                    ),
                    "last_updated": last_updated,
                    "data": None,
                    "error": (
                        "Invalid max_distance_km."
                    ),
                }

            if max_distance_km < 0:
                return {
                    "status": "UNAVAILABLE",
                    "source": (
                        "USNIC Antarctic Iceberg Dataset"
                    ),
                    "last_updated": last_updated,
                    "data": None,
                    "error": (
                        "max_distance_km cannot be negative."
                    ),
                }

            nearby = get_nearby_icebergs_with_distance(
                icebergs,
                latitude,
                longitude,
                max_distance_km
            )

        else:
            # Existing loader returns prepared data.
            nearby = icebergs

        # ----------------------------------------------------
        # Convert DataFrame to list if required
        # ----------------------------------------------------

        if hasattr(nearby, "to_dict"):

            try:
                nearby_data = nearby.to_dict(
                    orient="records"
                )
            except Exception:
                nearby_data = []

        elif isinstance(nearby, list):
            nearby_data = nearby

        else:
            nearby_data = []

        return {
            "status": "LIVE",
            "source": (
                "USNIC Antarctic Iceberg Dataset"
            ),
            "last_updated": last_updated,
            "data": {
                "icebergs": nearby_data,
                "count": len(nearby_data),
            },
            "error": None,
        }

    except Exception as error:
        return {
            "status": "UNAVAILABLE",
            "source": (
                "USNIC Antarctic Iceberg Dataset"
            ),
            "last_updated": None,
            "data": None,
            "error": str(error),
        }


# ============================================================
# WEATHER + MARINE
# ============================================================

def fetch_environment(
    latitude,
    longitude
):
    """
    Fetch weather + marine data together.
    """

    weather = fetch_weather(
        latitude,
        longitude
    )

    marine = fetch_marine(
        latitude,
        longitude
    )

    statuses = [
        weather.get("status"),
        marine.get("status"),
    ]

    if all(
        status == "LIVE"
        for status in statuses
    ):
        overall_status = "LIVE"

    elif all(
        status == "UNAVAILABLE"
        for status in statuses
    ):
        overall_status = "UNAVAILABLE"

    elif any(
        status == "STALE"
        for status in statuses
    ):
        overall_status = "STALE"

    else:
        overall_status = "FALLBACK"

    return {
        "status": overall_status,
        "source": {
            "weather": weather.get(
                "source"
            ),
            "marine": marine.get(
                "source"
            ),
        },
        "last_updated": {
            "weather": weather.get(
                "last_updated"
            ),
            "marine": marine.get(
                "last_updated"
            ),
        },
        "data": {
            "weather": weather.get(
                "data"
            ),
            "marine": marine.get(
                "data"
            ),
        },
        "error": {
            "weather": weather.get(
                "error"
            ),
            "marine": marine.get(
                "error"
            ),
        },
    }


# ============================================================
# COMPLETE ENVIRONMENTAL DATA
# ============================================================

def fetch_all_environmental_data(
    latitude,
    longitude,
    sea_ice_date=None,
    iceberg_distance_km=100
):
    """
    Complete M3 environmental-data function.

    Returns one structured object for M4/M5.

    Sources:
        Weather -> Open-Meteo
        Marine  -> Open-Meteo
        Sea Ice -> NOAA/NSIDC
        Iceberg -> USNIC
    """

    weather = fetch_weather(
        latitude,
        longitude
    )

    marine = fetch_marine(
        latitude,
        longitude
    )

    sea_ice = fetch_sea_ice(
        latitude,
        longitude,
        sea_ice_date
    )

    icebergs = fetch_icebergs(
        latitude,
        longitude,
        iceberg_distance_km
    )

    statuses = [
        weather.get("status"),
        marine.get("status"),
        sea_ice.get("status"),
        icebergs.get("status"),
    ]

    # --------------------------------------------------------
    # Overall status
    # --------------------------------------------------------

    if all(
        status == "LIVE"
        for status in statuses
    ):
        overall_status = "LIVE"

    elif all(
        status == "UNAVAILABLE"
        for status in statuses
    ):
        overall_status = "UNAVAILABLE"

    elif any(
        status == "STALE"
        for status in statuses
    ):
        overall_status = "STALE"

    else:
        overall_status = "FALLBACK"

    # --------------------------------------------------------
    # Final M3 -> M4/M5 structure
    # --------------------------------------------------------

    return {
        "status": overall_status,

        "source": {
            "weather": weather.get(
                "source"
            ),
            "marine": marine.get(
                "source"
            ),
            "sea_ice": sea_ice.get(
                "source"
            ),
            "icebergs": icebergs.get(
                "source"
            ),
        },

        "last_updated": {
            "weather": weather.get(
                "last_updated"
            ),
            "marine": marine.get(
                "last_updated"
            ),
            "sea_ice": sea_ice.get(
                "last_updated"
            ),
            "icebergs": icebergs.get(
                "last_updated"
            ),
        },

        "data": {
            "weather": weather.get(
                "data"
            ),
            "marine": marine.get(
                "data"
            ),
            "sea_ice": sea_ice.get(
                "data"
            ),
            "icebergs": icebergs.get(
                "data"
            ),
        },

        "error": {
            "weather": weather.get(
                "error"
            ),
            "marine": marine.get(
                "error"
            ),
            "sea_ice": sea_ice.get(
                "error"
            ),
            "icebergs": icebergs.get(
                "error"
            ),
        },
    }


# ============================================================
# M5 READY FUNCTION
# ============================================================

def get_m5_environmental_input(
    latitude,
    longitude,
    sea_ice_date=None,
    iceberg_distance_km=100
):
    """
    Reusable clean function for M5.

    M5 can directly call this function.
    """

    result = fetch_all_environmental_data(
        latitude,
        longitude,
        sea_ice_date,
        iceberg_distance_km
    )

    return result


# ============================================================
# M4 READY FUNCTION
# ============================================================

def get_m4_environmental_input(
    latitude,
    longitude,
    sea_ice_date=None,
    iceberg_distance_km=100
):
    """
    Reusable clean function for M4 risk module.
    """

    result = fetch_all_environmental_data(
        latitude,
        longitude,
        sea_ice_date,
        iceberg_distance_km
    )

    return result


# ============================================================
# END OF FILE
# ============================================================