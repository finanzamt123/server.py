from flask import Flask, render_template, request, jsonify
import json
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = "data.json"
EC_DATA_FILE = "ec_data.csv"

# Standarddaten initialisieren
DEFAULT_DATA = {
    "calibration": {"ec_offset": 0},
    "schedules": {"watering": [], "ec_correction": []},
    "target_values": {"ec_target": 1000},
    "current_values": {"ec": 0, "water_temp": 0, "air_temp": 0}
}

# JSON-Datei initialisieren
if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
    with open(DATA_FILE, "w") as file:
        json.dump(DEFAULT_DATA, file, indent=4)

# EC-Daten initialisieren
if not os.path.exists(EC_DATA_FILE):
    with open(EC_DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "ec_value"])

# Lade Daten aus JSON
def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

# Speichere Daten in JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Route für die Hauptseite
@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)

# Route zum Aktualisieren der Zeitpläne
@app.route("/update_schedule", methods=["POST"])
def update_schedule():
    data = load_data()
    payload = request.json
    schedule_type = payload.get("type")  # "watering" oder "ec_correction"
    new_schedule = payload.get("schedule", [])
    if schedule_type in data["schedules"]:
        data["schedules"][schedule_type] = new_schedule
        save_data(data)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid schedule type"}), 400

# Route für den Graphen
@app.route("/ec_graph_data")
def ec_graph_data():
    try:
        with open(EC_DATA_FILE, "r") as file:
            reader = csv.DictReader(file)
            data = [{"timestamp": row["timestamp"], "ec_value": float(row["ec_value"])} for row in reader]
            cutoff = datetime.now() - timedelta(hours=24)
            filtered_data = [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) >= cutoff]
            return jsonify(filtered_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route zum Speichern neuer EC-Werte
@app.route("/save_ec_value", methods=["POST"])
def save_ec_value():
    payload = request.json
    ec_value = payload.get("ec_value")
    timestamp = datetime.now().isoformat()
    with open(EC_DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ec_value])
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
