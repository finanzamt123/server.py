from flask import Flask, render_template, request, jsonify
import json
import os
import time
from datetime import datetime
# Zusätzliche Änderungen im SETTINGS-Standardwert
SETTINGS = {
    "ec_target": 2000,  # Ziel-EC-Wert in µS/cm
    "calibration": 0,  # Kalibrierungswert
    "watering_schedule": [],  # Gießplan: Liste mit Uhrzeit und Dauer
    "ec_correction_schedule": []  # EC-Korrektur: Liste mit Uhrzeit und Dauer
}

app = Flask(__name__)

SETTINGS_FILE = "settings.json"
SENSOR_LOG_FILE = "sensor_data.json"  # Datei für Sensordaten

# Laden oder Erstellen der JSON-Datei
try:
    with open(SETTINGS_FILE, "r") as file:
        SETTINGS = json.load(file)
except FileNotFoundError:
    SETTINGS = {
        "ec_target": 2000,  # Standard-Zielwert in µS/cm
        "water_schedule": "08:00, 20:00",
        "calibration": 0  # Standardkalibrierwert
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(SETTINGS, file)

# Sensor-Daten-Log initialisieren
if not os.path.exists(SENSOR_LOG_FILE):
    with open(SENSOR_LOG_FILE, "w") as file:
        json.dump([], file)

# Route: Anzeige der Website
@app.route("/")
def index():
    with open(SENSOR_LOG_FILE, "r") as file:
        sensor_data = json.load(file)
    latest_data = sensor_data[-1] if sensor_data else {"water_temp": 0, "tds": 0}  # Letzter Eintrag
    return render_template("index.html", data={"settings": SETTINGS, "sensor_data": latest_data})

# Route: Sensor-Daten empfangen
@app.route("/update_sensor_data", methods=["POST"])
def update_sensor_data():
    new_data = request.get_json()
    if new_data:
        new_data["timestamp"] = int(time.time())
        with open(SENSOR_LOG_FILE, "r+") as file:
            data = json.load(file)
            data.append(new_data)  # Neue Daten anhängen
            # Nur die letzten 24 Stunden behalten
            cutoff = int(time.time()) - 86400
            data = [entry for entry in data if entry["timestamp"] > cutoff]
            file.seek(0)
            file.truncate()
            json.dump(data, file)
    return "OK"

# Route: Sensordaten abrufen
@app.route("/get_sensor_data", methods=["GET"])
def get_sensor_data():
    with open(SENSOR_LOG_FILE, "r") as file:
        data = json.load(file)
    return jsonify(data)

# Route: Einstellungen aktualisieren
# Route: Einstellungen aktualisieren
@app.route("/update_settings", methods=["POST"])
def update_settings():
    new_settings = request.get_json()
    if new_settings:
        SETTINGS.update(new_settings)
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS)

# Route: Gießplan aktualisieren
@app.route("/update_watering_schedule", methods=["POST"])
def update_watering_schedule():
    new_schedule = request.get_json()
    if new_schedule:
        SETTINGS["watering_schedule"] = new_schedule
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS["watering_schedule"])

# Route: EC-Korrekturplan aktualisieren
@app.route("/update_ec_correction_schedule", methods=["POST"])
def update_ec_correction_schedule():
    new_schedule = request.get_json()
    if new_schedule:
        SETTINGS["ec_correction_schedule"] = new_schedule
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS["ec_correction_schedule"])

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
