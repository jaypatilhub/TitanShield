def preprocess_sea_ice(sea_ice_value):
    """
    Clean and standardize sea-ice concentration data.

    Input:
        sea_ice_value = raw sea-ice concentration in percentage

    Output:
        Standardized dictionary for M4/M5
    """

    # Handle missing data
    if sea_ice_value is None:
        return {
            "sea_ice_concentration": None,
            "data_status": "MISSING"
        }

    # Convert to number
    try:
        sea_ice_value = float(sea_ice_value)
    except (TypeError, ValueError):
        return {
            "sea_ice_concentration": None,
            "data_status": "INVALID"
        }

    # Validate range
    if sea_ice_value < 0 or sea_ice_value > 100:
        return {
            "sea_ice_concentration": None,
            "data_status": "INVALID"
        }

    # Standardized output
    return {
        "sea_ice_concentration": round(sea_ice_value, 2),
        "data_status": "VALID"
    }

def standardize_environmental_data(
    sea_ice_concentration=None,
    iceberg_distance=None,
    wind_speed=None,
    wave_height=None
):
    """
    Standardize environmental data for M4 and M5.
    """

    return {
        "sea_ice_concentration": sea_ice_concentration,
        "iceberg_distance": iceberg_distance,
        "wind_speed": wind_speed,
        "wave_height": wave_height
    }

def validate_environmental_data(data):
    """
    Validate standardized environmental data.
    """

    errors = []

    sea_ice = data.get("sea_ice_concentration")
    iceberg_distance = data.get("iceberg_distance")
    wind_speed = data.get("wind_speed")
    wave_height = data.get("wave_height")

    # Sea-ice validation
    if sea_ice is not None:
        if not isinstance(sea_ice, (int, float)):
            errors.append("sea_ice_concentration must be numeric")
        elif sea_ice < 0 or sea_ice > 100:
            errors.append("sea_ice_concentration must be between 0 and 100")

    # Iceberg distance validation
    if iceberg_distance is not None:
        if not isinstance(iceberg_distance, (int, float)):
            errors.append("iceberg_distance must be numeric")
        elif iceberg_distance < 0:
            errors.append("iceberg_distance cannot be negative")

    # Wind speed validation
    if wind_speed is not None:
        if not isinstance(wind_speed, (int, float)):
            errors.append("wind_speed must be numeric")
        elif wind_speed < 0:
            errors.append("wind_speed cannot be negative")

    # Wave height validation
    if wave_height is not None:
        if not isinstance(wave_height, (int, float)):
            errors.append("wave_height must be numeric")
        elif wave_height < 0:
            errors.append("wave_height cannot be negative")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
def clean_environmental_data(data):
    """
    Clean environmental data before sending it to M4/M5.
    Converts numeric values and marks invalid/missing values.
    """

    cleaned = {}

    fields = [
        "sea_ice_concentration",
        "iceberg_distance",
        "wind_speed",
        "wave_height"
    ]

    for field in fields:
        value = data.get(field)

        # Missing value
        if value is None:
            cleaned[field] = None
            continue

        # Convert numeric strings to numbers
        try:
            value = float(value)
        except (TypeError, ValueError):
            cleaned[field] = None
            continue

        # Reject negative values
        if value < 0:
            cleaned[field] = None
            continue

        # Sea-ice must be 0–100%
        if field == "sea_ice_concentration" and value > 100:
            cleaned[field] = None
            continue

        cleaned[field] = round(value, 2)

    return cleaned

def preprocess_environmental_data(data):
    """
    Complete M3 preprocessing pipeline.
    Cleans and validates environmental data.
    """

    cleaned_data = clean_environmental_data(data)
    validation = validate_environmental_data(cleaned_data)

    return {
        "data": cleaned_data,
        "validation": validation
    }
def get_model_input(data):
    """
    Prepare clean environmental data for M4 and M5.
    """

    return {
        "sea_ice_concentration": data.get("sea_ice_concentration"),
        "iceberg_distance": data.get("iceberg_distance"),
        "wind_speed": data.get("wind_speed"),
        "wave_height": data.get("wave_height")
    }
def get_m4_input(data):
    """
    Prepare standardized environmental data for M4 risk module.
    """

    return {
        "sea_ice_concentration": data.get("sea_ice_concentration"),
        "iceberg_distance": data.get("iceberg_distance"),
        "wind_speed": data.get("wind_speed"),
        "wave_height": data.get("wave_height")
    }
def prepare_data_for_ai(data):
    """
    Complete M3 pipeline for M4/M5.
    Clean -> Validate -> Prepare AI input.
    """

    cleaned_data = clean_environmental_data(data)
    validation = validate_environmental_data(cleaned_data)

    if not validation["valid"]:
        return {
            "status": "INVALID",
            "data": None,
            "errors": validation["errors"]
        }

    ai_input = get_m4_input(cleaned_data)

    return {
        "status": "READY",
        "data": ai_input,
        "errors": []
    }