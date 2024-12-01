import random
import time

def generate_air_quality_data():
    while True:
        air_quality_index = random.randint(0, 500)  # Random AQI value
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        print(f"Time: {timestamp}, AQI: {air_quality_index}")
        time.sleep(2)  # Simulates new data every 2 seconds

generate_air_quality_data()
