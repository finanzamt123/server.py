from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Pfad zur Datenbankdatei
DATA_FILE = "data/data.json"

# Sicherstellen, dass die Datei existiert
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Route: Empfang von Sensordaten
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json  # JSON-Daten empfangen
    if not data:
        return "Keine Daten empfangen", 400

    # Daten in Datei speichern
    with open(DATA_FILE, "r+") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

        existing_data.append(data)
        f.seek(0)
        json.dump(existing_data, f, indent=4)

    return "Daten erfolgreich gespeichert", 200

# Route: Daten anzeigen
@app.route('/view')
def view_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

# Hauptseite
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
