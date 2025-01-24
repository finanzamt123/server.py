from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"
EC_DATA_FILE = "ec_graph/ec_data.csv"

# Initiale Daten laden oder erstellen
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({
            "current_values": {"ec": 0, "water_temp": 0, "air_temp": 0},
            "calibration": {"ec_offset": 0},
            "schedules": {"watering": [], "ec_correction": []}
        }, f)

# Daten laden
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Daten speichern
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Routen
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)

@app.route("/update_sensors", methods=["POST"])
def update_sensors():
    data = load_data()
    sensors = request.json
    data["current_values"].update(sensors)
    save_data(data)

    # Historische Daten speichern
    with open(EC_DATA_FILE, "a") as f:
        f.write(f"{datetime.now()},{sensors['ec']}\n")
    return jsonify({"success": True})

@app.route("/update_settings", methods=["POST"])
def update_settings():
    data = load_data()
    updates = request.json
    for key, value in updates.items():
        if key in data:
            data[key].update(value)
    save_data(data)
    return jsonify({"success": True})

@app.route("/update_schedule", methods=["POST"])
def update_schedule():
    data = load_data()
    schedule_type = request.json["type"]
    new_schedule = request.json["schedule"]
    if schedule_type in data["schedules"]:
        data["schedules"][schedule_type] = new_schedule
        save_data(data)
        return jsonify({"success": True})
    return jsonify({"error": "Invalid schedule type"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
