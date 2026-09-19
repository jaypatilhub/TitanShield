# =========================================================
# ANTARCTIC AI - M5 DATA ADAPTER
# M5 - Khushi
# Connects M3 environmental data with M5
# =========================================================

from m3_live_data import get_m5_environmental_input


def get_navigation_data(
    latitude,
    longitude,
    sea_ice_date=None,
    iceberg_distance_km=100
):
    """
    Get the existing M3 environmental data for M5.

    M3 is responsible for data fetching.
    M5 only consumes and passes through the returned
    environmental structure without modifying its schema.
    """

    navigation_data = get_m5_environmental_input(
        latitude=latitude,
        longitude=longitude,
        sea_ice_date=sea_ice_date,
        iceberg_distance_km=iceberg_distance_km
    )

    return navigation_data