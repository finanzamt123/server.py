const serverUrl = "http://192.168.178.57:5000";

function fetchData() {
    fetch(`${serverUrl}/get_data`)
    .then(response => response.json())
    .then(data => {
        document.getElementById("ecValue").textContent = data.ec.toFixed(2);
        document.getElementById("waterTemp").textContent = data.water_temp.toFixed(1);
        document.getElementById("airTemp").textContent = data.air_temp.toFixed(1);
        document.getElementById("calibrationFactor").textContent = data.calibration_factor.toFixed(2);
    });
}

function calibrate() {
    const knownEC = parseFloat(document.getElementById("knownEC").value);
    if (knownEC) {
        fetch(`${serverUrl}/calibrate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ known_ec: knownEC }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("calibrationStatus").textContent = data.message;
            fetchData();
        });
    }
}

function updateSettings() {
    const ecFrequency = parseInt(document.getElementById("ecFrequency").value);
    const wateringFrequency = parseInt(document.getElementById("wateringFrequency").value);
    const wateringDuration = parseInt(document.getElementById("wateringDuration").value);

    fetch(`${serverUrl}/update_settings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            ec_correction_frequency: ecFrequency,
            watering_frequency: wateringFrequency,
            watering_duration: wateringDuration,
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("settingsStatus").textContent = data.message;
    });
}

setInterval(fetchData, 10000);
fetchData();
