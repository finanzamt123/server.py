import json
from flask import Flask, render_template, request

app = Flask(__name__)

# Pfad zur JSON-Datei, in der die Einstellungen gespeichert werden
settings_file = 'settings.json'


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


def save_settings(settings):
    with open(settings_file, 'w') as file:
        json.dump(settings, file)


@app.route('/')
def index():
    # Lade die aktuellen Einstellungen aus der Datei
    settings = load_settings()
    return render_template('index.html', settings=settings)


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

    return render_template('index.html', settings=settings)


if __name__ == '__main__':
    app.run(debug=True)
