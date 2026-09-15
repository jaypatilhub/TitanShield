# =========================================================
# ANTARCTIC AI - ROUTE OPTIMIZATION MODULE
# M5 - Khushi
# =========================================================
def calculate_route_score(distance_km, risk_score, fuel_cost):
    """
    Calculate a balanced score for route comparison.

    Lower score = better route.
    Risk has the highest importance, followed by distance and fuel.
    """

    distance_score = distance_km / 1000
    fuel_score = fuel_cost / 100000

    score = (
        distance_score * 0.3
        + risk_score * 0.5
        + fuel_score * 0.2
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
            "risk_level": "HIGH",
            "travel_time_hours": 12,
            "route_coordinates": []
        },
        {
            "name": "Route B",
            "distance_km": 3950,
            "risk_score": 45,
            "fuel_cost": 790000,
            "risk_level": "MEDIUM",
            "travel_time_hours": 13,
            "route_coordinates": []
        },
        {
            "name": "Route C",
            "distance_km": 4100,
            "risk_score": 20,
            "fuel_cost": 820000,
            "risk_level": "LOW",
            "travel_time_hours": 14,
            "route_coordinates": []
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
def dynamic_reroute(routes, current_route_name):
    """
    Recalculate the best route when the current route
    becomes unsafe due to new hazard information.
    """

    current_route = next(
        (route for route in routes if route["name"] == current_route_name),
        None
    )

    if current_route is None:
        return None

    if current_route["risk_level"] in ["HIGH", "CRITICAL"]:
        for route in routes:
            route["score"] = calculate_route_score(
                route["distance_km"],
                route["risk_score"],
                route["fuel_cost"]
            )

        safer_routes = [
            route for route in routes
            if route["risk_level"] not in ["HIGH", "CRITICAL"]
        ]

        if safer_routes:
            return min(safer_routes, key=lambda route: route["score"])

    return current_route