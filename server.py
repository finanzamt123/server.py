import flask
from flask import request, jsonify, render_template
import json

app = flask.Flask(__name__)

# Globale Variablen
current_data = {
    "ec": 0.0,
    "water_temp": 0.0,
    "air_temp": 0.0,
    "calibration_factor": 1.0,
}
settings = {
    "ec_correction_frequency": 1,
    "watering_frequency": 1,
    "watering_duration": 10,
}

# Lade gespeicherte Einstellungen
def load_settings():
    global settings
    try:
        with open("config.json", "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        save_settings()

# Speichere Einstellungen
def save_settings():
    with open("config.json", "w") as file:
        json.dump(settings, file)

# Startseite
@app.route("/")
def index():
    return render_template("index.html")

# Route für aktuelle Daten
@app.route("/get_data", methods=["GET"])
def get_data():
    return jsonify(current_data)

# Route zum Aktualisieren von Messdaten
@app.route("/update_data", methods=["POST"])
def update_data():
    global current_data
    data = request.get_json()
    if data:
        current_data.update(data)
        return jsonify({"message": "Daten aktualisiert"}), 200
    return jsonify({"error": "Ungültige Daten"}), 400

# Route für Kalibrierung
@app.route("/calibrate", methods=["POST"])
def calibrate():
    data = request.get_json()
    if "known_ec" in data:
        current_data["calibration_factor"] = data["known_ec"] / current_data["ec"]
        return jsonify({"message": "Kalibrierung erfolgreich"}), 200
    return jsonify({"error": "Kein EC-Wert angegeben"}), 400

# Route zum Aktualisieren von Einstellungen
@app.route("/update_settings", methods=["POST"])
def update_settings():
    global settings
    data = request.get_json()
    if data:
        settings.update(data)
        save_settings()
        return jsonify({"message": "Einstellungen aktualisiert"}), 200
    return jsonify({"error": "Ungültige Daten"}), 400

# Lade Einstellungen beim Start
load_settings()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
