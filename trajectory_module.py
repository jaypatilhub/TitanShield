# =========================================================
# ANTARCTIC AI - ICEBERG MOVEMENT & TRAJECTORY MODULE
# M4 - Rutuja
# =========================================================

from math import atan2, asin, cos, radians, sin, sqrt, degrees
from datetime import datetime


def calculate_movement(previous_latitude, previous_longitude,
                       current_latitude, current_longitude,
                       previous_time, current_time):
    """
    Calculate iceberg movement speed and direction.

    Input:
        Previous and current iceberg positions
        Previous and current observation timestamps

    Output:
        Movement speed in km/h
        Movement direction in degrees
    """

    # Convert coordinates to float
    previous_latitude = float(previous_latitude)
    previous_longitude = float(previous_longitude)
    current_latitude = float(current_latitude)
    current_longitude = float(current_longitude)

    # Convert timestamps
    previous_time = datetime.fromisoformat(previous_time)
    current_time = datetime.fromisoformat(current_time)

    time_difference_hours = (
        current_time - previous_time
    ).total_seconds() / 3600

    if time_difference_hours <= 0:
        raise ValueError(
            "Current observation time must be after previous observation time."
        )

    # Earth radius in kilometres
    earth_radius = 6371.0

    # Convert coordinates to radians
    lat1 = radians(previous_latitude)
    lat2 = radians(current_latitude)
    lon1 = radians(previous_longitude)
    lon2 = radians(current_longitude)

    # Haversine distance
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = earth_radius * c

    # Movement speed
    speed_kmh = distance_km / time_difference_hours

    # Calculate movement direction
    y = sin(delta_lon) * cos(lat2)

    x = (
        cos(lat1) * sin(lat2)
        - sin(lat1) * cos(lat2) * cos(delta_lon)
    )

    direction = (degrees(atan2(y, x)) + 360) % 360

    return {
        "distance_km": round(distance_km, 3),
        "speed_kmh": round(speed_kmh, 3),
        "direction_degrees": round(direction, 2)
    }
    
    
def predict_future_position(latitude, longitude,
                            speed_kmh, direction_degrees,
                            hours_ahead):
    """
    Predict iceberg position after a given number of hours.

    Input:
        latitude: current latitude
        longitude: current longitude
        speed_kmh: movement speed
        direction_degrees: movement direction
        hours_ahead: prediction time in hours

    Output:
        predicted latitude and longitude
    """

    if hours_ahead < 0:
        raise ValueError("Prediction time cannot be negative.")

    earth_radius = 6371.0

    latitude = radians(float(latitude))
    longitude = radians(float(longitude))

    distance_km = float(speed_kmh) * float(hours_ahead)
    bearing = radians(float(direction_degrees))

    angular_distance = distance_km / earth_radius

    predicted_latitude = asin(
        sin(latitude) * cos(angular_distance)
        + cos(latitude)
        * sin(angular_distance)
        * cos(bearing)
    )

    predicted_longitude = longitude + atan2(
        sin(bearing) * sin(angular_distance) * cos(latitude),
        cos(angular_distance)
        - sin(latitude) * sin(predicted_latitude)
    )

    predicted_latitude = degrees(predicted_latitude)
    predicted_longitude = degrees(predicted_longitude)

    return {
        "latitude": round(predicted_latitude, 6),
        "longitude": round(predicted_longitude, 6)
    }
    
    
def generate_trajectory(latitude, longitude,
                        speed_kmh, direction_degrees):
    """
    Generate predicted iceberg positions for
    6, 12, 24 and 48 hours.
    """

    prediction_hours = [6, 12, 24, 48]

    trajectory = {}

    for hours in prediction_hours:
        trajectory[f"{hours}h"] = predict_future_position(
            latitude,
            longitude,
            speed_kmh,
            direction_degrees,
            hours
        )

    return trajectory


def get_trajectory_assessment(
    iceberg_id,
    latitude,
    longitude,
    speed_kmh,
    direction_degrees,
    source="UNKNOWN"
):
    """
    Return the complete M4 iceberg trajectory assessment.
    """

    if latitude is None or longitude is None:
        return {
            "iceberg_id": iceberg_id,
            "status": "UNAVAILABLE",
            "reason": "Current iceberg position is unavailable."
        }

    if speed_kmh is None or direction_degrees is None:
        return {
            "iceberg_id": iceberg_id,
            "status": "UNAVAILABLE",
            "reason": "Iceberg movement information is unavailable."
        }

    trajectory = generate_trajectory(
        latitude,
        longitude,
        speed_kmh,
        direction_degrees
    )

    return {
        "iceberg_id": iceberg_id,

        "current_position": {
            "latitude": latitude,
            "longitude": longitude
        },

        "movement": {
            "direction_degrees": direction_degrees,
            "speed_kmh": speed_kmh
        },

        "trajectory": trajectory,

        "confidence": "BASIC_PROJECTION",

        "source": source,

        "status": "AVAILABLE"
    }
    
    
def build_trajectory_from_observations(
    iceberg_id,
    previous_latitude,
    previous_longitude,
    previous_timestamp,
    current_latitude,
    current_longitude,
    current_timestamp,
    source="UNKNOWN"
):
    """
    Build iceberg trajectory from two observed positions.
    """

    movement = calculate_movement(
        previous_latitude,
        previous_longitude,
        current_latitude,
        current_longitude,
        previous_timestamp,
        current_timestamp
    )

    return get_trajectory_assessment(
        iceberg_id=iceberg_id,
        latitude=current_latitude,
        longitude=current_longitude,
        speed_kmh=movement["speed_kmh"],
        direction_degrees=movement["direction_degrees"],
        source=source
    )