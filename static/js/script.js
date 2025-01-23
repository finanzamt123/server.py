document.addEventListener("DOMContentLoaded", function () {
    const updateInterval = 5000; // Update alle 5 Sekunden
    const sensorEndpoint = "/get_sensor_data";
    const ecChartCtx = document.getElementById("ecChart").getContext("2d");

    let ecChart = new Chart(ecChartCtx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "EC-Wert (µS/cm)",
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 2,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Zeit" } },
                y: { title: { display: true, text: "EC-Wert (µS/cm)" } }
            }
        }
    });

    async function fetchSensorData() {
        try {
            const response = await fetch(sensorEndpoint);
            const data = await response.json();

            // Aktuelle Werte
            const latest = data[data.length - 1] || { water_temp: 0, tds: 0 };
            document.getElementById("waterTemp").textContent = `${latest.water_temp} °C`;
            document.getElementById("ecValue").textContent = `${latest.tds} µS/cm`;

            // Graph-Daten aktualisieren
            ecChart.data.labels = data.map(entry => new Date(entry.timestamp * 1000).toLocaleTimeString());
            ecChart.data.datasets[0].data = data.map(entry => entry.tds);
            ecChart.update();
        } catch (error) {
            console.error("Fehler beim Abrufen der Sensordaten:", error);
        }
    }
    // Hinzufügen eines neuen Eintrags zum Gießplan
function addWateringEntry() {
    const time = prompt("Bitte Uhrzeit eingeben (HH:MM):");
    const duration = prompt("Bitte Dauer in Minuten eingeben:");
    if (time && duration) {
        fetch("/update_watering_schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ time, duration }),
        })
            .then(response => response.json())
            .then(updateWateringScheduleTable)
            .catch(console.error);
    }
}

// Löschen eines Eintrags aus dem Gießplan
function deleteWateringEntry(index) {
    fetch("/update_watering_schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ deleteIndex: index }),
    })
        .then(response => response.json())
        .then(updateWateringScheduleTable)
        .catch(console.error);
}

// Aktualisierung der Tabelle Gießplan
function updateWateringScheduleTable(schedule) {
    const tableBody = document.querySelector("#wateringScheduleTable tbody");
    tableBody.innerHTML = schedule
        .map(
            (entry, index) => `
        <tr>
            <td>${entry.time}</td>
            <td>${entry.duration}</td>
            <td><button onclick="deleteWateringEntry(${index})">Löschen</button></td>
        </tr>`
        )
        .join("");
}

// Hinzufügen eines neuen Eintrags zur EC-Korrektur
function addECCorrectionEntry() {
    const time = prompt("Bitte Uhrzeit eingeben (HH:MM):");
    const duration = prompt("Bitte Dauer in Minuten eingeben:");
    if (time && duration) {
        fetch("/update_ec_correction_schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ time, duration }),
        })
            .then(response => response.json())
            .then(updateECCorrectionScheduleTable)
            .catch(console.error);
    }
}

// Löschen eines Eintrags aus der EC-Korrektur
function deleteECCorrectionEntry(index) {
    fetch("/update_ec_correction_schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ deleteIndex: index }),
    })
        .then(response => response.json())
        .then(updateECCorrectionScheduleTable)
        .catch(console.error);
}

// Aktualisierung der Tabelle EC-Korrektur
function updateECCorrectionScheduleTable(schedule) {
    const tableBody = document.querySelector("#ecCorrectionScheduleTable tbody");
    tableBody.innerHTML = schedule
        .map(
            (entry, index) => `
        <tr>
            <td>${entry.time}</td>
            <td>${entry.duration}</td>
            <td><button onclick="deleteECCorrectionEntry(${index})">Löschen</button></td>
        </tr>`
        )
        .join("");
}


    setInterval(fetchSensorData, updateInterval);
    fetchSensorData();
});
