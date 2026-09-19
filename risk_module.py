# =========================================================
# ANTARCTIC AI - RISK INTELLIGENCE MODULE
# M4 + M5 Integration
# Uses the existing M3 environmental data structure
# =========================================================


# ---------------------------------------------------------
# SEA-ICE RISK
# ---------------------------------------------------------

def calculate_sea_ice_risk(sea_ice_concentration):
    """
    Calculate sea-ice risk from the available M3 sea-ice value.
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


# ---------------------------------------------------------
# ICEBERG RISK
# ---------------------------------------------------------

def calculate_iceberg_risk(distance_km):
    """
    Calculate iceberg risk using the nearest available
    iceberg distance from the M3 dataset.
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


# ---------------------------------------------------------
# WEATHER RISK
# ---------------------------------------------------------

def calculate_weather_risk(
    wind_speed,
    wave_height=None,
    precipitation=None
):
    """
    Calculate weather risk from available M3 weather and
    marine parameters.
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


# ---------------------------------------------------------
# OCEAN / MARINE RISK
# ---------------------------------------------------------

def calculate_ocean_marine_risk(
    wave_height=None,
    ocean_current_velocity=None
):
    """
    Calculate marine risk using real M3 marine data.

    M3 may provide:
    - wave_height_m
    - ocean_current_velocity_kmh

    If neither value is available, report UNAVAILABLE.
    No environmental value is fabricated.
    """

    if wave_height is None and ocean_current_velocity is None:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Ocean/marine data is currently unavailable."
        }

    scores = []
    reasons = []

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

    if ocean_current_velocity is not None:

        if ocean_current_velocity > 5:
            scores.append(75)
            reasons.append("High ocean-current velocity.")

        elif ocean_current_velocity >= 3:
            scores.append(50)
            reasons.append("Moderate ocean-current velocity.")

        else:
            scores.append(20)
            reasons.append("Low ocean-current velocity.")

    if not scores:
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "reason": "Ocean/marine data is currently unavailable."
        }

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


# ---------------------------------------------------------
# ICEBERG TRAJECTORY RISK
# ---------------------------------------------------------

def calculate_iceberg_trajectory_risk(
    current_distance_km,
    future_distance_km=None
):
    """
    Calculate iceberg trajectory risk.

    Future trajectory remains UNAVAILABLE when M3 does not
    provide future trajectory information.
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
            "reason": (
                "Future iceberg trajectory data is currently unavailable."
            )
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


# ---------------------------------------------------------
# OVERALL RISK
# ---------------------------------------------------------

def calculate_overall_risk(
    sea_ice_risk,
    iceberg_risk,
    weather_risk,
    trajectory_risk,
    ocean_risk=None
):
    """
    Calculate overall navigation risk from all available
    risk components.
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
        "reason": (
            "Overall risk is based on the highest available "
            "hazard score."
        )
    }


# ---------------------------------------------------------
# RISK HAZARDS
# ---------------------------------------------------------

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
        named_components.append(
            ("Ocean/marine", ocean_risk)
        )

    for name, component in named_components:

        level = component.get("risk_level")

        if level in ["HIGH", "CRITICAL"]:
            hazards.append(
                f"{name} risk: "
                f"{component.get('reason', 'Hazard detected.')}"
            )

    if not hazards:
        hazards.append(
            "No high or critical hazard detected "
            "from available data."
        )

    return hazards


# ---------------------------------------------------------
# COMPLETE RISK ASSESSMENT
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# M3 -> M5 RISK INTEGRATION
# ---------------------------------------------------------

def build_navigation_risk(navigation_data):
    """
    Convert the existing M3 environmental structure into
    the M5 navigation risk assessment.

    M3 schema is preserved.
    """

    if not isinstance(navigation_data, dict):
        return {
            "risk_score": None,
            "risk_level": "UNAVAILABLE",
            "safety_score": None,
            "hazards": [
                "M3 environmental input is unavailable."
            ],
            "components": {},
            "explanation": (
                "No valid M3 environmental input was provided."
            ),
            "m3_environment": None
        }

    data = navigation_data.get("data") or {}

    weather = data.get("weather") or {}
    marine = data.get("marine") or {}
    sea_ice = data.get("sea_ice") or {}
    iceberg_data = data.get("icebergs") or {}

    # -----------------------------------------------------
    # SEA-ICE
    # -----------------------------------------------------

    sea_ice_concentration = None

    if isinstance(sea_ice, dict):
        sea_ice_concentration = sea_ice.get(
            "concentration"
        )

        if sea_ice_concentration is None:
            sea_ice_concentration = sea_ice.get(
                "sea_ice_concentration"
            )

    sea_ice_risk = calculate_sea_ice_risk(
        sea_ice_concentration
    )

    # -----------------------------------------------------
    # ICEBERGS
    # -----------------------------------------------------

    nearest_iceberg_distance = None
    nearest_iceberg = None

    if isinstance(iceberg_data, dict):

        iceberg_list = iceberg_data.get(
            "icebergs"
        ) or []

        valid_icebergs = [
            iceberg
            for iceberg in iceberg_list
            if isinstance(iceberg, dict)
            and iceberg.get("distance_km") is not None
        ]

        if valid_icebergs:
            nearest_iceberg = min(
                valid_icebergs,
                key=lambda iceberg: iceberg.get("distance_km")
            )

            nearest_iceberg_distance = nearest_iceberg.get(
                "distance_km"
            )

    iceberg_risk = calculate_iceberg_risk(
        nearest_iceberg_distance
    )

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    wind_speed = None
    precipitation = None

    if isinstance(weather, dict):
        wind_speed = weather.get(
            "wind_speed_kmh"
        )

        precipitation = weather.get(
            "precipitation"
        )

    # -----------------------------------------------------
    # MARINE
    # -----------------------------------------------------

    wave_height = None
    ocean_current_velocity = None

    if isinstance(marine, dict):
        wave_height = marine.get(
            "wave_height_m"
        )

        ocean_current_velocity = marine.get(
            "ocean_current_velocity_kmh"
        )

    weather_risk = calculate_weather_risk(
        wind_speed=wind_speed,
        wave_height=wave_height,
        precipitation=precipitation
    )

    # -----------------------------------------------------
    # TRAJECTORY
    # -----------------------------------------------------

    trajectory_risk = calculate_iceberg_trajectory_risk(
        nearest_iceberg_distance,
        future_distance_km=None
    )

    # -----------------------------------------------------
    # OCEAN / MARINE
    # -----------------------------------------------------

    ocean_risk = calculate_ocean_marine_risk(
        wave_height=wave_height,
        ocean_current_velocity=ocean_current_velocity
    )

    # -----------------------------------------------------
    # FINAL ASSESSMENT
    # -----------------------------------------------------

    assessment = generate_risk_assessment(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk,
        ocean_risk
    )

    # Preserve M3 metadata without modifying the M3 object.
    assessment["m3_environment"] = {
        "status": navigation_data.get("status"),
        "source": navigation_data.get("source"),
        "last_updated": navigation_data.get(
            "last_updated"
        ),
        "error": navigation_data.get("error")
    }

    return assessment