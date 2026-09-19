# =========================================================
# ANTARCTIC AI - RISK INTELLIGENCE MODULE
# M4 + M5 Integration
# =========================================================

def calculate_sea_ice_risk(sea_ice_concentration):
    """
    Calculate sea-ice risk.
    Real value is required; unavailable data is reported honestly.
    """

    if sea_ice_concentration is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Sea-ice concentration data is currently unavailable."
        }

    if sea_ice_concentration >= 90:
        return {
            "risk_score": 95,
            "risk_level": "CRITICAL",
            "reason": "Very high sea-ice concentration."
        }

    if sea_ice_concentration >= 75:
        return {
            "risk_score": 75,
            "risk_level": "HIGH",
            "reason": "High sea-ice concentration."
        }

    if sea_ice_concentration >= 50:
        return {
            "risk_score": 50,
            "risk_level": "MEDIUM",
            "reason": "Moderate sea-ice concentration."
        }

    return {
        "risk_score": 20,
        "risk_level": "LOW",
        "reason": "Low sea-ice concentration."
    }


def calculate_iceberg_risk(distance_km):
    """
    Calculate iceberg risk using the nearest detected iceberg.
    """

    if distance_km is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "No iceberg distance available."
        }

    if distance_km <= 5:
        return {
            "risk_score": 95,
            "risk_level": "CRITICAL",
            "reason": f"Nearest iceberg is only {distance_km:.2f} km away."
        }

    if distance_km <= 15:
        return {
            "risk_score": 75,
            "risk_level": "HIGH",
            "reason": f"Nearest iceberg is {distance_km:.2f} km away."
        }

    if distance_km <= 30:
        return {
            "risk_score": 45,
            "risk_level": "MEDIUM",
            "reason": f"Nearest iceberg is {distance_km:.2f} km away."
        }

    return {
        "risk_score": 15,
        "risk_level": "LOW",
        "reason": f"Nearest detected iceberg is {distance_km:.2f} km away."
    }


def calculate_weather_risk(wind_speed, wave_height=None, precipitation=None):
    """
    Calculate weather risk from available weather parameters.

    M3 currently provides wind speed and precipitation.
    Wave height is optional because it is not currently supplied by M3.
    """

    if wind_speed is None and wave_height is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Weather risk inputs are unavailable."
        }

    scores = []
    reasons = []

    if wind_speed is not None:
        if wind_speed > 50:
            scores.append(95)
            reasons.append("Very high wind speed.")
        elif wind_speed >= 35:
            scores.append(75)
            reasons.append("High wind speed.")
        elif wind_speed >= 20:
            scores.append(50)
            reasons.append("Moderate wind speed.")
        else:
            scores.append(20)
            reasons.append("Low wind speed.")

    if wave_height is not None:
        if wave_height > 6:
            scores.append(95)
            reasons.append("Very high wave height.")
        elif wave_height >= 4:
            scores.append(75)
            reasons.append("High wave height.")
        elif wave_height >= 2:
            scores.append(50)
            reasons.append("Moderate wave height.")
        else:
            scores.append(20)
            reasons.append("Low wave height.")

    risk_score = max(scores)

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
        "reason": " ".join(reasons)
    }


def calculate_iceberg_trajectory_risk(
    current_distance_km,
    future_distance_km=None
):
    """
    Calculate iceberg trajectory risk.

    Future trajectory is marked unavailable because the current
    M3 iceberg dataset provides position data but not future trajectory.
    """

    if current_distance_km is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Current iceberg distance is unavailable."
        }

    if future_distance_km is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Future iceberg trajectory data is currently unavailable."
        }

    if future_distance_km <= 5:
        level = "CRITICAL"
        score = 95
    elif future_distance_km <= 15:
        level = "HIGH"
        score = 75
    elif future_distance_km <= 30:
        level = "MEDIUM"
        score = 50
    else:
        level = "LOW"
        score = 20

    if future_distance_km < current_distance_km:
        movement = "Iceberg is approaching the vessel route."
    elif future_distance_km > current_distance_km:
        movement = "Iceberg is moving away from the vessel route."
    else:
        movement = "Iceberg distance is unchanged."

    return {
        "risk_score": score,
        "risk_level": level,
        "reason": movement
    }


def calculate_ocean_marine_risk():
    """
    Ocean/marine risk component.

    No ocean-current or wave-height dataset is currently available
    in the M3 pipeline, so the system does not fabricate a value.
    """

    return {
        "risk_score": None,
        "risk_level": "UNAVAILABLE",
        "reason": "Ocean/marine data is currently unavailable."
    }


def calculate_overall_risk(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk,
    ocean_risk=None
):
    """
    Calculate overall navigation risk using available risk components.
    """

    components = [
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk
    ]

    if ocean_risk is not None:
        components.append(ocean_risk)

    available_scores = [
        component["risk_score"]
        for component in components
        if component.get("risk_score") is not None
    ]

    if not available_scores:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "No usable risk component is currently available."
        }

    risk_score = max(available_scores)

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
        "reason": "Overall risk is based on the highest available hazard score."
    }


def get_risk_hazards(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk,
    ocean_risk=None
):
    """
    Return explainable navigation hazards.
    """

    hazards = []

    named_components = [
        ("Sea-ice", sea_ice_risk),
        ("Iceberg", iceberg_risk),
        ("Weather", weather_risk),
        ("Iceberg trajectory", trajectory_risk)
    ]

    if ocean_risk is not None:
        named_components.append(("Ocean/marine", ocean_risk))

    for name, component in named_components:
        level = component.get("risk_level")

        if level in ["HIGH", "CRITICAL"]:
            hazards.append(
                f"{name} risk: {component.get('reason', 'Hazard detected.')}"
            )

    if not hazards:
        hazards.append("No high or critical hazard detected from available data.")

    return hazards


def generate_risk_assessment(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk,
    ocean_risk=None
):
    """
    Generate complete explainable navigation risk assessment.
    """

    overall_risk = calculate_overall_risk(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk,
        ocean_risk
    )

    hazards = get_risk_hazards(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk,
        ocean_risk
    )

    risk_score = overall_risk["risk_score"]

    safety_score = (
        round(100 - risk_score, 2)
        if risk_score is not None
        else None
    )

    return {
        "risk_score": risk_score,
        "risk_level": overall_risk["risk_level"],
        "safety_score": safety_score,
        "hazards": hazards,
        "components": {
            "sea_ice": sea_ice_risk,
            "iceberg": iceberg_risk,
            "weather": weather_risk,
            "trajectory": trajectory_risk,
            "ocean_marine": ocean_risk
        },
        "explanation": overall_risk["reason"]
    }


def build_navigation_risk(navigation_data):
    """
    Convert M3 data adapter output into the M4 risk assessment.
    """

    weather = navigation_data.get("weather") or {}
    iceberg = navigation_data.get("iceberg") or {}
    sea_ice = navigation_data.get("sea_ice") or {}

    sea_ice_risk = calculate_sea_ice_risk(
        sea_ice.get("concentration")
    )

    iceberg_risk = calculate_iceberg_risk(
        iceberg.get("nearest_distance_km")
    )

    weather_risk = calculate_weather_risk(
        weather.get("wind_speed"),
        wave_height=None,
        precipitation=weather.get("precipitation")
    )

    trajectory_risk = calculate_iceberg_trajectory_risk(
        iceberg.get("nearest_distance_km"),
        future_distance_km=None
    )

    ocean_risk = calculate_ocean_marine_risk()

    return generate_risk_assessment(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk,
        ocean_risk
    )