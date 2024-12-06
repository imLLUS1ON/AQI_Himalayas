from flask import Flask, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

# Load .env file to access the API key
load_dotenv()

# Specify the template folder explicitly
app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")


# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

# Location data
LOCATIONS = {
    "Kedarnath": {"lat": 30.734627, "lon": 79.066895},
    "Badrinath": {"lat": 30.7433, "lon": 79.4938},
    "Rudranath": {"lat": 30.53333, "lon": 79.33333}
}

@app.route('/')
def home():
    return render_template('index.html')  # Render the frontend

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
        return jsonify({
            "location": location,
            "AQI": data["list"][0]["main"]["aqi"],
            "details": data["list"][0]["components"]
        })
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
