from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"settings": {}, "sensor_data": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

@app.route("/")
def index():
    data = load_data()
    return render_template("index.html", data=data)

@app.route("/update_sensor_data", methods=["POST"])
def update_sensor_data():
    data = load_data()
    data["sensor_data"] = request.json
    save_data(data)
    return "OK", 200

@app.route("/update_settings", methods=["POST"])
def update_settings():
    data = load_data()
    data["settings"] = request.json
    save_data(data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
