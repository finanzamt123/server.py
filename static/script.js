const serverUrl = "http://192.168.178.57:5000";

function fetchData() {
    fetch(`${serverUrl}/get_data`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("waterTemp").innerText = data.sensor_data.water_temperature;
            document.getElementById("airTemp").innerText = data.sensor_data.air_temperature;
            document.getElementById("ecValue").innerText = data.sensor_data.ec_value;
        });
}

function saveSettings() {
    const ecTarget = parseFloat(document.getElementById("ecTarget").value);
    const ecFrequency = parseInt(document.getElementById("ecFrequency").value);
    const waterFrequency = parseInt(document.getElementById("waterFrequency").value);
    const waterDuration = parseInt(document.getElementById("waterDuration").value);

    fetch(`${serverUrl}/update_config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            ec_target: ecTarget,
            ec_correction_frequency: ecFrequency,
            watering_frequency: waterFrequency,
            watering_duration: waterDuration
        })
    });
}

function calibrate() {
    const knownEC = parseFloat(document.getElementById("knownEC").value);

    fetch(`${serverUrl}/calibrate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ known_ec: knownEC })
    }).then(response => response.json())
      .then(data => alert(data.message));
}

setInterval(fetchData, 10000); // Aktualisierung alle 10 Sekunden
