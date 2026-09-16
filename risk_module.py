
# =========================================================
# ANTARCTIC AI - AI RISK INTELLIGENCE MODULE
# M4 - Rutuja
# =========================================================


def calculate_sea_ice_risk(sea_ice_concentration):
    """
    Calculate navigation risk based on sea-ice concentration.

    Input:
        sea_ice_concentration: percentage from 0 to 100

    Output:
        risk_score: 0 to 100
        risk_level: LOW / MEDIUM / HIGH / CRITICAL
    """

    if sea_ice_concentration >= 90:
        risk_score = 95
        risk_level = "CRITICAL"

    elif sea_ice_concentration >= 75:
        risk_score = 75
        risk_level = "HIGH"

    elif sea_ice_concentration >= 50:
        risk_score = 50
        risk_level = "MEDIUM"

    else:
        risk_score = 20
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reason": f"Sea-ice concentration is {sea_ice_concentration}%."
    }


def calculate_iceberg_risk(distance_km):
    """
    Calculate navigation risk based on distance
    from the nearest iceberg.

    Input:
        distance_km: distance from vessel to nearest iceberg in km

    Output:
        risk_score: 0 to 100
        risk_level: LOW / MEDIUM / HIGH / CRITICAL
    """

    if distance_km <= 5:
        risk_score = 95
        risk_level = "CRITICAL"

    elif distance_km <= 15:
        risk_score = 75
        risk_level = "HIGH"

    elif distance_km <= 30:
        risk_score = 45
        risk_level = "MEDIUM"

    else:
        risk_score = 15
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reason": f"Nearest iceberg is {distance_km} km away."
    }


def calculate_weather_risk(wind_speed, wave_height):
    """
    Calculate navigation risk based on wind speed
    and wave height.

    Input:
        wind_speed: km/h
        wave_height: meters

    Output:
        risk_score: 0 to 100
        risk_level: LOW / MEDIUM / HIGH / CRITICAL
    """

    # Wind risk
    if wind_speed > 50:
        wind_score = 95
    elif wind_speed >= 35:
        wind_score = 75
    elif wind_speed >= 20:
        wind_score = 50
    else:
        wind_score = 20

    # Wave risk
    if wave_height > 6:
        wave_score = 95
    elif wave_height >= 4:
        wave_score = 75
    elif wave_height >= 2:
        wave_score = 50
    else:
        wave_score = 20

    # Take the higher risk
    risk_score = max(wind_score, wave_score)

    if risk_score >= 90:
        risk_level = "CRITICAL"
    elif risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reason": f"Wind speed is {wind_speed} km/h and wave height is {wave_height} m."
    }


def calculate_iceberg_trajectory_risk(current_distance_km, future_distance_km):
    """
    Calculate navigation risk based on predicted future
    distance of an iceberg from the research vessel.

    Input:
        current_distance_km: current distance from vessel
        future_distance_km: predicted future distance from vessel

    Output:
        risk_score: 0 to 100
        risk_level: LOW / MEDIUM / HIGH / CRITICAL
    """

    if current_distance_km < 0 or future_distance_km < 0:
        raise ValueError("Distance cannot be negative.")


    if future_distance_km <= 5:
        risk_score = 95
        risk_level = "CRITICAL"

    elif future_distance_km <= 15:
        risk_score = 75
        risk_level = "HIGH"

    elif future_distance_km <= 30:
        risk_score = 50
        risk_level = "MEDIUM"

    else:
        risk_score = 20
        risk_level = "LOW"

    if future_distance_km < current_distance_km:
        movement_reason = "Iceberg is approaching the vessel."

    elif future_distance_km > current_distance_km:
        movement_reason = "Iceberg is moving away from the vessel."

    else:
        movement_reason = "Iceberg distance is expected to remain unchanged."

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reason": (
    f"{movement_reason} "
    f"Distance is expected to change "
    f"from {current_distance_km} km to "
    f"{future_distance_km} km."
)
    }


def calculate_overall_risk(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk
):
    """
    Combine all individual risk assessments
    and return the highest overall risk.
    """

    risk_scores = [
        sea_ice_risk["risk_score"],
        iceberg_risk["risk_score"],
        weather_risk["risk_score"],
        trajectory_risk["risk_score"]
    ]

    overall_score = max(risk_scores)

    if overall_score >= 90:
        overall_level = "CRITICAL"

    elif overall_score >= 70:
        overall_level = "HIGH"

    elif overall_score >= 40:
        overall_level = "MEDIUM"

    else:
        overall_level = "LOW"

    return {
        "risk_score": overall_score,
        "risk_level": overall_level,
        "reason": "Overall risk is based on the highest individual navigation risk."
    }


def get_risk_hazards(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk
):
    """
    Identify the main hazards responsible for navigation risk.
    """

    hazards = []

    if sea_ice_risk["risk_level"] in ["HIGH", "CRITICAL"]:
        hazards.append("High sea-ice concentration")

    if iceberg_risk["risk_level"] in ["HIGH", "CRITICAL"]:
        hazards.append("Iceberg is too close to the vessel")

    if weather_risk["risk_level"] in ["HIGH", "CRITICAL"]:
        hazards.append("Unsafe weather conditions")

    if trajectory_risk["risk_level"] in ["HIGH", "CRITICAL"]:
        hazards.append(trajectory_risk["reason"])

    return hazards


def generate_risk_assessment(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk
):
    """
    Generate final AI risk assessment
    by combining all navigation risk factors.
    """

    overall_risk = calculate_overall_risk(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk
    )

    hazards = get_risk_hazards(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk
    )

    return {
        "risk_score": overall_risk["risk_score"],
        "risk_level": overall_risk["risk_level"],
        "hazards": hazards,

        "components": {
            "sea_ice": sea_ice_risk,
            "iceberg": iceberg_risk,
            "weather": weather_risk,
            "trajectory": trajectory_risk
        },

        "reason": overall_risk["reason"]
    }
