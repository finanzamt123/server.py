import flask
import json
from flask import request, jsonify, render_template
from flask import Flask, render_template, request
import json

app = flask.Flask(__name__)
settings_file = 'settings.json'

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
    try:
        with open(settings_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Falls die Datei noch nicht existiert, wird sie mit Standardwerten erstellt
        return {
            'ec_value': 0.0,
            'water_temp': 0.0,
            'watering_time': 10,
            'watering_interval': 3
        }
# Speichere Einstellungen
def save_settings(settings):
    with open(settings_file, 'w') as file:
        json.dump(settings, file)

# Startseite
@app.route('/')
def index():
    # Lade die aktuellen Einstellungen aus der Datei
    settings = load_settings()
    return render_template('index.html', settings=settings)


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


@app.route('/update_settings', methods=['POST'])
def update_settings():
    # Holen der neuen Werte aus dem Formular
    ec_value = request.form.get('ec_value')
    water_temp = request.form.get('water_temp')
    watering_time = request.form.get('watering_time')
    watering_interval = request.form.get('watering_interval')

    # Werte in einem Dictionary speichern
    settings = {
        'ec_value': float(ec_value),
        'water_temp': float(water_temp),
        'watering_time': int(watering_time),
        'watering_interval': int(watering_interval)
    }

    # Speichern der neuen Einstellungen in der JSON-Datei
    save_settings(settings)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
