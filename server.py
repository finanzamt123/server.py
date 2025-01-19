import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Datei zum Speichern der Parameter
PARAMS_FILE = "data/params.json"
os.makedirs(os.path.dirname(PARAMS_FILE), exist_ok=True)

# Standardwerte
target_ec = 2.0
correction_interval = 60

# Lade die gespeicherten Parameter, falls vorhanden
if os.path.isfile(PARAMS_FILE):
    with open(PARAMS_FILE, "r") as f:
        try:
            params = json.load(f)
            target_ec = params.get("target_ec", target_ec)
            correction_interval = params.get("interval", correction_interval)
        except json.JSONDecodeError:
            pass

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return "Keine Daten empfangen", 400
    
    # Sensordaten speichern...
    return "Daten erfolgreich gespeichert", 200

@app.route('/view')
def view_data():
    # Sensordaten anzeigen...
    return jsonify({"target_ec": target_ec, "interval": correction_interval})

@app.route('/control', methods=['GET'])
def control_pump():
    # Pumpensteuerung basierend auf EC-Wert...
    return "EIN"  # Beispielantwort

@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    global target_ec, correction_interval

    data = request.json
    if not data:
        return "Keine Daten erhalten", 400

    # Ziel-EC-Wert und Korrekturintervall aktualisieren
    target_ec = data.get('target_ec', target_ec)
    correction_interval = data.get('interval', correction_interval)

    # Speichern der neuen Parameter in der Datei
    with open(PARAMS_FILE, "w") as f:
        json.dump({
            "target_ec": target_ec,
            "interval": correction_interval
        }, f, indent=4)

    return jsonify({
        "message": "Parameter erfolgreich aktualisiert",
        "target_ec": target_ec,
        "interval": correction_interval
    }), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
