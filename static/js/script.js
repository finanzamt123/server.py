document.addEventListener("DOMContentLoaded", function () {
    const updateInterval = 5000; // Update alle 5 Sekunden
    const sensorEndpoint = "/update_sensor_data";

    async function fetchSensorData() {
        try {
            const response = await fetch(sensorEndpoint);
            const data = await response.json();

            document.getElementById("waterTemp").textContent = `${data.water_temp} °C`;
            document.getElementById("ecValue").textContent = `${data.tds} ppm`;
        } catch (error) {
            console.error("Fehler beim Abrufen der Sensordaten:", error);
        }
    }

    setInterval(fetchSensorData, updateInterval);
});
