from iceberg.loader import (
    load_antarctic_icebergs,
    prepare_iceberg_data,
    get_nearby_icebergs_with_distance
)

data = load_antarctic_icebergs(
    "data/AntarcticIcebergs_20260910.csv"
)

data = prepare_iceberg_data(data)


# TEST 1: Missing coordinates
print("\nTEST 1 - Missing coordinates")

try:
    get_nearby_icebergs_with_distance(
        data,
        None,
        None,
        100
    )
except ValueError as error:
    print("PASS:", error)


# TEST 2: Invalid latitude
print("\nTEST 2 - Invalid latitude")

try:
    get_nearby_icebergs_with_distance(
        data,
        -100,
        -50,
        100
    )
except ValueError as error:
    print("PASS:", error)


# TEST 3: Invalid longitude
print("\nTEST 3 - Invalid longitude")

try:
    get_nearby_icebergs_with_distance(
        data,
        -60,
        200,
        100
    )
except ValueError as error:
    print("PASS:", error)


# TEST 4: Negative distance
print("\nTEST 4 - Negative distance")

try:
    get_nearby_icebergs_with_distance(
        data,
        -60,
        -50,
        -10
    )
except ValueError as error:
    print("PASS:", error)