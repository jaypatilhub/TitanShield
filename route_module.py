# =========================================================
# ANTARCTIC AI - ROUTE OPTIMIZATION MODULE
# M5 - Khushi
# =========================================================

from math import radians, sin, cos, sqrt, atan2


# ---------------------------------------------------------
# CONFIGURABLE VESSEL PARAMETERS
# ---------------------------------------------------------

DEFAULT_VESSEL_SPEED_KNOTS = 12
DEFAULT_FUEL_RATE_LPH = 250


# ---------------------------------------------------------
# DISTANCE CALCULATION
# ---------------------------------------------------------

def calculate_distance_km(point1, point2):
    """
    Calculate great-circle distance between two coordinates.

    point format:
        (latitude, longitude)
    """

    lat1, lon1 = point1
    lat2, lon2 = point2

    earth_radius_km = 6371.0

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(earth_radius_km * c, 2)


def calculate_route_distance(route_coordinates):
    """
    Calculate total distance along a route.
    """

    if len(route_coordinates) < 2:
        return 0.0

    total_distance = 0.0

    for index in range(len(route_coordinates) - 1):
        total_distance += calculate_distance_km(
            route_coordinates[index],
            route_coordinates[index + 1]
        )

    return round(total_distance, 2)


# ---------------------------------------------------------
# ROUTE GENERATION
# ---------------------------------------------------------

def generate_candidate_routes(start, destination):
    """
    Generate three candidate routes using different
    intermediate waypoints.

    Route geometry is generated from the given start
    and destination, not hardcoded as a recommendation.
    """

    start_lat, start_lon = start
    dest_lat, dest_lon = destination

    mid_lat = (start_lat + dest_lat) / 2
    mid_lon = (start_lon + dest_lon) / 2

    lat_difference = abs(dest_lat - start_lat)
    lon_difference = abs(dest_lon - start_lon)

    # Three different navigation corridors
    route_a_mid = (
        mid_lat + lat_difference * 0.20,
        mid_lon - lon_difference * 0.10
    )

    route_b_mid = (
        mid_lat,
        mid_lon
    )

    route_c_mid = (
        mid_lat - lat_difference * 0.20,
        mid_lon + lon_difference * 0.10
    )

    routes = [
        {
            "name": "Route A",
            "route_coordinates": [
                start,
                route_a_mid,
                destination
            ]
        },
        {
            "name": "Route B",
            "route_coordinates": [
                start,
                route_b_mid,
                destination
            ]
        },
        {
            "name": "Route C",
            "route_coordinates": [
                start,
                route_c_mid,
                destination
            ]
        }
    ]

    return routes


# ---------------------------------------------------------
# POINT TO ROUTE APPROXIMATION
# ---------------------------------------------------------

def minimum_distance_to_route(point, route_coordinates):
    """
    Approximate the minimum distance from a hazard point
    to the route using route waypoints.

    This keeps the calculation simple and explainable.
    """

    distances = [
        calculate_distance_km(point, route_point)
        for route_point in route_coordinates
    ]

    return min(distances)


# ---------------------------------------------------------
# ROUTE RISK
# ---------------------------------------------------------

def calculate_route_risk(route, risk_context):
    """
    Calculate route-specific risk using available
    real navigation data.

    The nearest iceberg position comes from the M3 dataset.
    """

    base_risk = risk_context.get("risk_score")

    if base_risk is None:
        base_risk = 0

    iceberg_data = risk_context.get("iceberg") or {}
    nearest_iceberg = iceberg_data.get("nearest_iceberg")

    route_risk = float(base_risk)

    iceberg_distance = None

    if nearest_iceberg:
        iceberg_point = (
            nearest_iceberg["latitude"],
            nearest_iceberg["longitude"]
        )

        iceberg_distance = minimum_distance_to_route(
            iceberg_point,
            route["route_coordinates"]
        )

        if iceberg_distance <= 5:
            route_risk = max(route_risk, 95)

        elif iceberg_distance <= 15:
            route_risk = max(route_risk, 75)

        elif iceberg_distance <= 30:
            route_risk = max(route_risk, 50)

        elif iceberg_distance <= 100:
            route_risk = max(route_risk, 30)

    if route_risk >= 90:
        risk_level = "CRITICAL"

    elif route_risk >= 70:
        risk_level = "HIGH"

    elif route_risk >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": round(route_risk, 2),
        "risk_level": risk_level,
        "nearest_iceberg_to_route_km": (
            round(iceberg_distance, 2)
            if iceberg_distance is not None
            else None
        )
    }


# ---------------------------------------------------------
# FUEL ESTIMATION
# ---------------------------------------------------------

def estimate_fuel(
    distance_km,
    vessel_speed_knots=DEFAULT_VESSEL_SPEED_KNOTS,
    fuel_rate_lph=DEFAULT_FUEL_RATE_LPH
):
    """
    Estimate travel time and fuel consumption.

    Fuel rate is configurable because no vessel-specific
    fuel-consumption dataset is currently available.
    """

    speed_kmh = vessel_speed_knots * 1.852

    if speed_kmh <= 0:
        return {
            "travel_time_hours": None,
            "fuel_liters": None,
            "fuel_rate_lph": fuel_rate_lph
        }

    travel_time_hours = distance_km / speed_kmh

    fuel_liters = travel_time_hours * fuel_rate_lph

    return {
        "travel_time_hours": round(travel_time_hours, 2),
        "fuel_liters": round(fuel_liters, 2),
        "fuel_rate_lph": fuel_rate_lph
    }


# ---------------------------------------------------------
# ROUTE SCORE
# ---------------------------------------------------------

def calculate_route_score(
    distance_km,
    risk_score,
    fuel_cost
):
    """
    Calculate balanced route score.

    Lower score = better route.

    Safety has the highest weight.
    Distance and fuel are secondary factors.
    """

    distance_score = distance_km / 1000
    fuel_score = fuel_cost / 1000

    score = (
        distance_score * 0.20
        + risk_score * 0.60
        + fuel_score * 0.20
    )

    return round(score, 2)


# ---------------------------------------------------------
# EVALUATE ROUTES
# ---------------------------------------------------------

def evaluate_routes(
    routes,
    risk_context,
    vessel_speed_knots=DEFAULT_VESSEL_SPEED_KNOTS,
    fuel_rate_lph=DEFAULT_FUEL_RATE_LPH
):
    """
    Add distance, risk, travel time, fuel and score
    to every candidate route.
    """

    evaluated_routes = []

    for route in routes:

        distance_km = calculate_route_distance(
            route["route_coordinates"]
        )

        risk = calculate_route_risk(
            route,
            risk_context
        )

        fuel = estimate_fuel(
            distance_km,
            vessel_speed_knots,
            fuel_rate_lph
        )

        score = calculate_route_score(
            distance_km,
            risk["risk_score"],
            fuel["fuel_liters"]
        )

        evaluated_route = {
            **route,
            "distance_km": distance_km,
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"],
            "nearest_iceberg_to_route_km":
                risk["nearest_iceberg_to_route_km"],
            "travel_time_hours":
                fuel["travel_time_hours"],
            "fuel_liters":
                fuel["fuel_liters"],
            "fuel_rate_lph":
                fuel["fuel_rate_lph"],
            "score": score
        }

        evaluated_routes.append(evaluated_route)

    return evaluated_routes


# ---------------------------------------------------------
# BEST ROUTE RECOMMENDATION
# ---------------------------------------------------------

def recommend_best_route(routes):
    """
    Recommend the route with the lowest calculated score.

    No route is permanently preferred.
    """

    if not routes:
        return None

    return min(
        routes,
        key=lambda route: route["score"]
    )


# ---------------------------------------------------------
# DYNAMIC REROUTING
# ---------------------------------------------------------

def dynamic_reroute(
    routes,
    current_route_name,
    risk_context
):
    """
    Re-evaluate routes when navigation conditions change.

    If the current route becomes high/critical risk,
    the system selects the best available alternative.
    """

    evaluated_routes = evaluate_routes(
        routes,
        risk_context
    )

    current_route = next(
        (
            route for route in evaluated_routes
            if route["name"] == current_route_name
        ),
        None
    )

    if current_route is None:
        return recommend_best_route(evaluated_routes)

    if current_route["risk_level"] in [
        "HIGH",
        "CRITICAL"
    ]:
        safer_routes = [
            route
            for route in evaluated_routes
            if route["risk_level"]
            not in ["HIGH", "CRITICAL"]
        ]

        if safer_routes:
            return min(
                safer_routes,
                key=lambda route: route["score"]
            )

        return recommend_best_route(evaluated_routes)

    return current_route


# ---------------------------------------------------------
# COMPLETE ROUTE OPTIMIZATION
# ---------------------------------------------------------

def optimize_routes(
    start,
    destination,
    risk_context,
    vessel_speed_knots=DEFAULT_VESSEL_SPEED_KNOTS,
    fuel_rate_lph=DEFAULT_FUEL_RATE_LPH
):
    """
    Complete M5 route optimization pipeline.

    Flow:
        Start/Destination
              ↓
        Generate A/B/C
              ↓
        Calculate Distance
              ↓
        Calculate Risk
              ↓
        Estimate Fuel
              ↓
        Calculate Score
              ↓
        Recommend Best Route
    """

    candidate_routes = generate_candidate_routes(
        start,
        destination
    )

    evaluated_routes = evaluate_routes(
        candidate_routes,
        risk_context,
        vessel_speed_knots,
        fuel_rate_lph
    )

    best_route = recommend_best_route(
        evaluated_routes
    )

    return {
        "routes": evaluated_routes,
        "recommended_route": best_route,
        "optimization_status": "COMPLETED",
        "fuel_model": {
            "vessel_speed_knots": vessel_speed_knots,
            "fuel_rate_lph": fuel_rate_lph,
            "note": (
                "Fuel rate is a configurable vessel assumption "
                "because vessel-specific fuel data is not currently "
                "available in the M3 pipeline."
            )
        }
    }