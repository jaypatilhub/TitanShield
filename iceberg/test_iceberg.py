from iceberg.loader import (
    load_antarctic_icebergs,
    prepare_iceberg_data,
    get_nearby_icebergs_with_distance
)

data = load_antarctic_icebergs(
    "data/AntarcticIcebergs_20260910.csv"
)

data = prepare_iceberg_data(data)

# Test 1: Nearby iceberg
print("\nTEST 1 - Nearby iceberg")
result = get_nearby_icebergs_with_distance(
    data, -61.00, -50.50, 100
)
print(result)

# Test 2: No nearby iceberg
print("\nTEST 2 - No nearby iceberg")
result = get_nearby_icebergs_with_distance(
    data, -89.0, 0.0, 10
)
print(result)

# Test 3: Multiple nearby icebergs
print("\nTEST 3 - Multiple icebergs")
result = get_nearby_icebergs_with_distance(
    data, -61.0, -51.0, 1000
)
print("Count:", len(result))