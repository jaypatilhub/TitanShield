from datetime import datetime
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M1_FILE = ROOT / "data_api.py"

spec = importlib.util.spec_from_file_location("m1_data_api", M1_FILE)
m1_data_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m1_data_api)


def fetch_sea_ice(latitude, longitude, data_date=None):
    if data_date is None:
        data_date = datetime.utcnow()

    try:
        value = m1_data_api.get_sea_ice_for_date(
            data_date,
            latitude,
            longitude
        )

        if value is None:
            return {
                "source": "NOAA/NSIDC",
                "last_updated": None,
                "data_status": "UNAVAILABLE",
                "data": None
            }

        return {
            "source": "NOAA/NSIDC",
            "last_updated": data_date.isoformat(),
            "data_status": "LIVE",
            "data": {
                "sea_ice_concentration": round(value, 2)
            }
        }

    except Exception as error:
        return {
            "source": "NOAA/NSIDC",
            "last_updated": None,
            "data_status": "UNAVAILABLE",
            "data": None,
            "error": str(error)
        }