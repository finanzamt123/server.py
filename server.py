# Zusätzliche Änderungen im SETTINGS-Standardwert
SETTINGS = {
    "ec_target": 2000,  # Ziel-EC-Wert in µS/cm
    "calibration": 0,  # Kalibrierungswert
    "watering_schedule": [],  # Gießplan: Liste mit Uhrzeit und Dauer
    "ec_correction_schedule": []  # EC-Korrektur: Liste mit Uhrzeit und Dauer
}

# Route: Einstellungen aktualisieren
@app.route("/update_settings", methods=["POST"])
def update_settings():
    new_settings = request.get_json()
    if new_settings:
        SETTINGS.update(new_settings)
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS)

# Route: Gießplan aktualisieren
@app.route("/update_watering_schedule", methods=["POST"])
def update_watering_schedule():
    new_schedule = request.get_json()
    if new_schedule:
        SETTINGS["watering_schedule"] = new_schedule
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS["watering_schedule"])

# Route: EC-Korrekturplan aktualisieren
@app.route("/update_ec_correction_schedule", methods=["POST"])
def update_ec_correction_schedule():
    new_schedule = request.get_json()
    if new_schedule:
        SETTINGS["ec_correction_schedule"] = new_schedule
        with open(SETTINGS_FILE, "w") as file:
            json.dump(SETTINGS, file)
    return jsonify(SETTINGS["ec_correction_schedule"])
