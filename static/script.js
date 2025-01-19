document.addEventListener("DOMContentLoaded", () => {
    const temperatureSpan = document.getElementById("temperature");
    const ecSpan = document.getElementById("ec");
    const calibrationFactorSpan = document.getElementById("calibrationFactor");

    function fetchData() {
        fetch("/view")
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const latest = data[data.length - 1]; // Letzter Eintrag
                    temperatureSpan.textContent = latest.temperature.toFixed(1); // Temperatur aktualisieren
                    ecSpan.textContent = latest.ec.toFixed(2); // EC-Wert aktualisieren
                }
            })
            .catch(error => console.error("Fehler beim Abrufen der Daten:", error));
    }

    fetchData();
    setInterval(fetchData, 5000); // Alle 5 Sekunden neue Daten laden

    document.getElementById("calibrate-btn").addEventListener("click", () => {
        const factor = parseFloat(prompt("Neuen Kalibrierungsfaktor eingeben:"));
        if (!isNaN(factor)) {
            fetch("/calibrate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ factor })
            })
                .then(response => response.text())
                .then(responseText => {
                    alert(responseText);
                    calibrationFactorSpan.textContent = factor.toFixed(2); // Kalibrierungsfaktor aktualisieren
                })
                .catch(error => console.error("Fehler bei der Kalibrierung:", error));
        }
    });
});
