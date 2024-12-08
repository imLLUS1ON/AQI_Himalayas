from flask import Flask, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

# Load .env file to access the API key
load_dotenv()

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# Check if API key is loaded
if not API_KEY:
    print("Error: OpenWeather API key is missing!")

# Location data
LOCATIONS = {
    "Kedarnath": {"lat": 30.734627, "lon": 79.066895},
    "Badrinath": {"lat": 30.7433, "lon": 79.4938},
    "Rudranath": {"lat": 30.53333, "lon": 79.33333}
}

# Function to calculate Indian AQI
def calculate_indian_aqi(components):
    # Pollutant breakpoints for Indian AQI
    pollutant_ranges = {
        "pm2_5": [(0, 30), (31, 60), (61, 90), (91, 120), (121, 250)],
        "pm10": [(0, 50), (51, 100), (101, 250), (251, 350), (351, 430)],
        "no2": [(0, 40), (41, 80), (81, 180), (181, 280), (281, 400)],
        "so2": [(0, 40), (41, 80), (81, 380), (381, 800), (801, 1600)],
        "co": [(0, 1), (1.1, 2), (2.1, 10), (10.1, 17), (17.1, 34)],
        "o3": [(0, 50), (51, 100), (101, 168), (169, 208), (209, 748)]
    }

    aqi_values = []
    for pollutant, ranges in pollutant_ranges.items():
        if pollutant in components:
            value = components[pollutant]
            for i, (low, high) in enumerate(ranges):
                if low <= value <= high:
                    aqi_values.append((i + 1) * 50)
                    break

    # Debugging log
    print("Pollutants and calculated AQI sub-indices:", aqi_values)
    return max(aqi_values) if aqi_values else 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/air_quality/<location>')
def air_quality(location):
    if location not in LOCATIONS:
        return jsonify({"error": "Invalid location"}), 400

    latitude = LOCATIONS[location]["lat"]
    longitude = LOCATIONS[location]["lon"]
    url = f"{BASE_URL}?lat={latitude}&lon={longitude}&appid={API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        components = data["list"][0]["components"]
        
        # Correct CO scale; no conversion needed
        aqi_indian = calculate_indian_aqi(components)
        
        return jsonify({
            "location": location,
            "AQI": aqi_indian,  # Send AQI correctly
            "details": components
        })
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
