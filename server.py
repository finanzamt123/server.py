import flask
from flask import request, jsonify, render_template
import json

app = flask.Flask(__name__)

# Globale Variablen für Messwerte und Konfiguration
config = {
    "ec_correction_frequency": 1,  # Wie oft pro Tag EC-Wert korrigiert wird
    "watering_frequency": 1,       # Wie oft pro Tag gegossen wird
    "watering_duration": 10,       # Gießdauer in Sekunden
    "calibration_factor": 1.0,     # Kalibrierungsfaktor
    "ec_target": 1.5               # Ziel-EC-Wert
}

sensor_data = {
    "water_temperature": 0.0,
    "air_temperature": 0.0,
    "ec_value": 0.0
}

# Daten laden und speichern
def load_config():
    try:
        with open("config.json", "r") as f:
            global config
            config = json.load(f)
    except FileNotFoundError:
        pass

def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify({
        "sensor_data": sensor_data,
        "config": config
    })

@app.route("/update_config", methods=["POST"])
def update_config():
    global config
    data = request.get_json()
    config.update(data)
    save_config()
    return jsonify({"message": "Konfiguration aktualisiert"})

@app.route("/update_sensors", methods=["POST"])
def update_sensors():
    global sensor_data
    data = request.get_json()
    sensor_data.update(data)
    return jsonify({"message": "Sensordaten aktualisiert"})

@app.route("/calibrate", methods=["POST"])
def calibrate():
    global config, sensor_data
    data = request.get_json()
    if "known_ec" in data:
        known_ec = data["known_ec"]
        config["calibration_factor"] = known_ec / sensor_data["ec_value"] if sensor_data["ec_value"] != 0 else 1.0
        save_config()
        return jsonify({"message": "Kalibrierung erfolgreich"})
    return jsonify({"error": "Bekannter EC-Wert fehlt"}), 400

@app.route("/update_sensors", methods=["POST"])
def update_sensors():
    global sensor_data
    data = request.get_json()
    print(f"Empfangene Daten: {data}")  # Debug-Ausgabe
    sensor_data.update(data)
    return jsonify({"message": "Sensordaten aktualisiert"})

if __name__ == "__main__":
    load_config()
    app.run(host="0.0.0.0", port=5000, debug=True)
