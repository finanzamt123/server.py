document.addEventListener("DOMContentLoaded", () => {
    const ecSpan = document.getElementById("ec");
    const pumpStatusSpan = document.getElementById("pump-status");
    const calibrationFactorSpan = document.getElementById("calibrationFactor");
    const targetEcInput = document.getElementById("target-ec-input");
    const intervalInput = document.getElementById("interval-input");

    // Lade gespeicherte Parameter
    function loadParams() {
        fetch("/view")
            .then(response => response.json())
            .then(data => {
                targetEcInput.value = data.target_ec || 2.0;  // Standardwert: 2.0
                intervalInput.value = data.interval || 60;   // Standardwert: 60
                document.getElementById("target-ec").textContent = data.target_ec || 2.0;
                document.getElementById("pump-status").textContent = "Wird überprüft...";
            })
            .catch(error => console.error("Fehler beim Laden der Parameter:", error));
    }

    loadParams();
    setInterval(loadParams, 5000);  // Alle 5 Sekunden die Parameter neu laden

    // Speichere neue Parameter
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
