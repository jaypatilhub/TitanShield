import json
from pathlib import Path


CACHE_FILE = Path("data_api") / "weather_cache.json"


def save_to_cache(data):
    """
    Save latest successful API data locally.
    """

    CACHE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )


def load_from_cache():
    """
    Load previously saved API data.
    """

    if not CACHE_FILE.exists():
        return None

    try:
        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None