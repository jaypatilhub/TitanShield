import pandas as pd
from math import radians, sin, cos, sqrt, atan2


def load_antarctic_icebergs(file_path):
    """
    Load official Antarctic iceberg data.
    """
    data = pd.read_csv(file_path)
    return data


def prepare_iceberg_data(data):
    """
    Clean official USNIC Antarctic iceberg data
    for M4 risk analysis and M2 map visualization.
    """

    required_columns = [
        "Iceberg",
        "Length (NM)",
        "Width (NM)",
        "Latitude",
        "Longitude",
        "Area (sqKM)",
        "Last Update"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    clean_data = data[required_columns].copy()

    clean_data["Latitude"] = pd.to_numeric(
        clean_data["Latitude"],
        errors="coerce"
    )

    clean_data["Longitude"] = pd.to_numeric(
        clean_data["Longitude"],
        errors="coerce"
    )

    clean_data["Area (sqKM)"] = pd.to_numeric(
        clean_data["Area (sqKM)"],
        errors="coerce"
    )

    clean_data = clean_data.dropna(
        subset=["Latitude", "Longitude"]
    )

    clean_data = clean_data[
        (clean_data["Latitude"] >= -90)
        & (clean_data["Latitude"] <= 90)
        & (clean_data["Longitude"] >= -180)
        & (clean_data["Longitude"] <= 180)
    ]

    return clean_data


def find_nearby_icebergs(
    data,
    vessel_latitude,
    vessel_longitude,
    radius_degrees=5
):
    """
    Roughly find icebergs near vessel coordinates.
    """

    nearby = data[
        (abs(data["Latitude"] - vessel_latitude) <= radius_degrees)
        &
        (abs(data["Longitude"] - vessel_longitude) <= radius_degrees)
    ].copy()

    return nearby


def calculate_distance_km(
    vessel_latitude,
    vessel_longitude,
    iceberg_latitude,
    iceberg_longitude
):
    """
    Calculate actual vessel-to-iceberg distance
    using the Haversine formula.
    """

    earth_radius_km = 6371.0

    lat1 = radians(vessel_latitude)
    lat2 = radians(iceberg_latitude)

    delta_lat = radians(
        iceberg_latitude - vessel_latitude
    )

    delta_lon = radians(
        iceberg_longitude - vessel_longitude
    )

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(
        earth_radius_km * c,
        2
    )


def get_nearby_icebergs_with_distance(
    data,
    vessel_latitude,
    vessel_longitude,
    max_distance_km=100
):
    """
    Find nearby icebergs and calculate actual distance
    from the vessel.
    """

    # Validate vessel coordinates
    if vessel_latitude is None or vessel_longitude is None:
        raise ValueError(
            "Vessel coordinates are required."
        )

    if not (-90 <= vessel_latitude <= 90):
        raise ValueError(
            "Invalid vessel latitude."
        )

    if not (-180 <= vessel_longitude <= 180):
        raise ValueError(
            "Invalid vessel longitude."
        )

    if max_distance_km < 0:
        raise ValueError(
            "Maximum distance cannot be negative."
        )

    results = []

    for _, iceberg in data.iterrows():

        distance = calculate_distance_km(
            vessel_latitude,
            vessel_longitude,
            iceberg["Latitude"],
            iceberg["Longitude"]
        )

        if distance <= max_distance_km:
            results.append({
                "iceberg": iceberg["Iceberg"],
                "latitude": iceberg["Latitude"],
                "longitude": iceberg["Longitude"],
                "length_nm": iceberg["Length (NM)"],
                "width_nm": iceberg["Width (NM)"],
                "area_sqkm": iceberg["Area (sqKM)"],
                "last_update": iceberg["Last Update"],
                "distance_km": distance
            })

    return results


def get_m4_iceberg_input(
    data,
    vessel_latitude,
    vessel_longitude,
    max_distance_km=100
):
    """
    Prepare nearby iceberg information
    for M4 risk analysis.
    """

    nearby = get_nearby_icebergs_with_distance(
        data,
        vessel_latitude,
        vessel_longitude,
        max_distance_km
    )

    return {
        "icebergs": nearby,
        "count": len(nearby)
    }


def get_m2_iceberg_markers(
    data,
    vessel_latitude,
    vessel_longitude,
    max_distance_km=100
):
    """
    Prepare nearby iceberg data
    for M2 map visualization.
    """

    nearby = get_nearby_icebergs_with_distance(
        data,
        vessel_latitude,
        vessel_longitude,
        max_distance_km
    )

    markers = []

    for iceberg in nearby:
        markers.append({
            "name": iceberg["iceberg"],
            "lat": iceberg["latitude"],
            "lon": iceberg["longitude"],
            "size_sqkm": iceberg["area_sqkm"],
            "distance_km": iceberg["distance_km"],
            "last_update": iceberg["last_update"]
        })

    return markers