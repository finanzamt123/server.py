from flask import Flask, request, jsonify, render_template
import json
import os
import time

app = Flask(__name__)

# Daten und Kalibrierung
DATA_FILE = "data/data.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Kalibrierungsfaktor und Ziel EC-Wert
calibration_factor = 1.0
target_ec = 2.0  # Beispielzielwert für EC
correction_interval = 60  # Korrekturintervall in Sekunden
last_correction_time = time.time()

# Pumpensteuerung
pump_status = "AUS"

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return "Keine Daten empfangen", 400

    global calibration_factor
    data['ec'] *= calibration_factor  # EC-Wert kalibrieren

    # Speichern der Sensordaten
    with open(DATA_FILE, "r+") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

        existing_data.append(data)
        f.seek(0)
        json.dump(existing_data, f, indent=4)

    return "Daten erfolgreich gespeichert", 200

@app.route('/view')
def view_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/control', methods=['GET'])
def control_pump():
    global pump_status, last_correction_time, target_ec

    # Berechne, ob der EC-Wert angepasst werden muss
    current_time = time.time()
    if current_time - last_correction_time >= correction_interval:
        last_correction_time = current_time

        # Berechne den aktuellen EC-Wert
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if data:
                latest_data = data[-1]
                current_ec = latest_data["ec"]

                # Wenn der EC-Wert unter dem Zielwert liegt, Pumpe einschalten
                if current_ec < target_ec:
                    pump_status = "EIN"
                else:
                    pump_status = "AUS"

    return pump_status

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global calibration_factor
    new_factor = request.json.get("factor")
    if new_factor is not None:
        calibration_factor = float(new_factor)
        return f"Kalibrierung auf Faktor {calibration_factor} gesetzt", 200
    return "Kein Faktor angegeben", 400

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
