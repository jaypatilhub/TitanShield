
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
