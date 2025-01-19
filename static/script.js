document.addEventListener("DOMContentLoaded", () => {
    const ecSpan = document.getElementById("ec");
    const pumpStatusSpan = document.getElementById("pump-status");
    const calibrationFactorSpan = document.getElementById("calibrationFactor");
    const targetEcInput = document.getElementById("target-ec-input");
    const intervalInput = document.getElementById("interval-input");

    function fetchData() {
        fetch("/view")
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const latest = data[data.length - 1];
                    ecSpan.textContent = latest.ec.toFixed(2);
                }
            })
            .catch(error => console.error("Fehler beim Abrufen der Daten:", error));
    }

    fetchData();
    setInterval(fetchData, 5000); // Alle 5 Sekunden neue Daten laden

    function fetchPumpStatus() {
        fetch("/control")
            .then(response => response.text())
            .then(status => {
                pumpStatusSpan.textContent = status;
            })
            .catch(error => console.error("Fehler beim Abrufen des Pumpenstatus:", error));
    }

    fetchPumpStatus();
    setInterval(fetchPumpStatus, 5000);

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
                    calibrationFactorSpan.textContent = factor.toFixed(2);
                })
                .catch(error => console.error("Fehler bei der Kalibrierung:", error));
        }
    });

   document.getElementById("save-params-btn").addEventListener("click", () => {
    const targetEc = parseFloat(targetEcInput.value);
    const interval = parseInt(intervalInput.value);

    if (!isNaN(targetEc) && !isNaN(interval)) {
        fetch("/update_parameters", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target_ec: targetEc, interval: interval })
        })
            .then(response => response.json())
            .then(responseJson => {
                alert(responseJson.message);
            })
            .catch(error => console.error("Fehler beim Speichern der Parameter:", error));
    }
});

    
});
