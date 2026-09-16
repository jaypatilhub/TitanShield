from preprocessing import prepare_data_for_ai

data = {
    "sea_ice_concentration": "82.567",
    "iceberg_distance": "12.4",
    "wind_speed": "28",
    "wave_height": "3.456"
}

result = prepare_data_for_ai(data)

print("SIMULATION MODE")
print("M3 → AI OUTPUT:", result)