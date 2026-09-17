from pathlib import Path
from statistics import mean

from data_api import (
    get_sea_ice_at_location,
    classify_sea_ice
)


def get_historical_sea_ice(
    data_dir="data",
    latitude=-60.0,
    longitude=20.0
):
    """
    Read available NOAA NetCDF files and extract
    sea-ice concentration at the given location.
    """

    data_path = Path(data_dir)

    files = sorted(
        data_path.glob("sic_pss25_202609*.nc")
    )

    results = []

    for file_path in files:

        concentration = get_sea_ice_at_location(
            str(file_path),
            latitude,
            longitude
        )

        if concentration is not None:

            results.append({
                "date": file_path.name.split("_")[2],
                "concentration": concentration
            })

    return results


def forecast_sea_ice(values):
    """
    Simple baseline forecast using the average
    of available recent observations.
    """

    if not values:
        return {
            "forecast": None,
            "category": "UNKNOWN"
        }

    forecast = mean(values)

    forecast = max(
        0.0,
        min(100.0, forecast)
    )

    category = classify_sea_ice(forecast)

    return {
        "forecast": round(forecast, 1),
        "category": category
    }


def generate_sea_ice_forecast(
    data_dir="data",
    latitude=-60.0,
    longitude=20.0
):
    """
    Complete M2 flow:

    NOAA files
        ↓
    Historical sea-ice values
        ↓
    Baseline forecast
        ↓
    Forecast category
    """

    historical_data = get_historical_sea_ice(
        data_dir,
        latitude,
        longitude
    )

    values = [
        item["concentration"]
        for item in historical_data
    ]

    forecast = forecast_sea_ice(values)

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "historical_data": historical_data,
        "forecast": forecast["forecast"],
        "category": forecast["category"]
    }


if __name__ == "__main__":

    result = generate_sea_ice_forecast()

    print()
    print("================================")
    print("      ANTARCTIC AI FORECAST")
    print("================================")

    print(
        f"Location: "
        f"{result['location']['latitude']}°, "
        f"{result['location']['longitude']}°"
    )

    print()
    print("Historical NOAA Data:")

    for item in result["historical_data"]:

        print(
            f"{item['date']} "
            f"-> {item['concentration']:.1f}%"
        )

    print()
    print(
        f"Forecast: "
        f"{result['forecast']}%"
    )

    print(
        f"Category: "
        f"{result['category']}"
    )

    print("================================")