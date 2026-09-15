# =========================================================
# ANTARCTIC AI - ROUTE OPTIMIZATION MODULE
# M5 - Khushi
# =========================================================

def calculate_route_score(distance_km, risk_score, fuel_cost):
    """
    Calculate a combined score for route comparison.

    Lower score = better route.
    """

    score = (
        distance_km * 0.4
        + risk_score * 0.4
        + fuel_cost * 0.2
    )

    return round(score, 2)
def generate_candidate_routes(start, destination):
    """
    Generate three candidate navigation routes
    between a fixed start and destination.
    """

    routes = [
        {
            "name": "Route A",
            "distance_km": 3800,
            "risk_score": 80,
            "fuel_cost": 760000,
            "risk_level": "HIGH"
        },
        {
            "name": "Route B",
            "distance_km": 3950,
            "risk_score": 45,
            "fuel_cost": 790000,
            "risk_level": "MEDIUM"
        },
        {
            "name": "Route C",
            "distance_km": 4100,
            "risk_score": 20,
            "fuel_cost": 820000,
            "risk_level": "LOW"
        }
    ]

    return routes
def recommend_best_route(routes):
    """
    Select the safest and most efficient route
    using the calculated route score.
    """

    for route in routes:
        route["score"] = calculate_route_score(
            route["distance_km"],
            route["risk_score"],
            route["fuel_cost"]
        )

    best_route = min(routes, key=lambda route: route["score"])

    return best_route