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

    setInterval(fetchSensorData, updateInterval);
    fetchSensorData();
});
