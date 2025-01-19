from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = "data/data.json"

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

calibration_factor = 1.0  # Standard-Kalibrierungsfaktor

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return "Keine Daten empfangen", 400

    global calibration_factor
    data['ec'] *= calibration_factor  # EC-Wert kalibrieren

    with open(DATA_FILE, "r+") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

        existing_data.append(data)
        f.seek(0)
        json.dump(existing_data, f, indent=4)

    return "Daten erfolgreich gespeichert", 200

@app.route('/calibrate', methods=['POST'])
def calibrate():
    global calibration_factor
    new_factor = request.json.get("factor")
    if new_factor is not None:
        calibration_factor = float(new_factor)
        return f"Kalibrierung auf Faktor {calibration_factor} gesetzt", 200
    return "Kein Faktor angegeben", 400

@app.route('/view')
def view_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
