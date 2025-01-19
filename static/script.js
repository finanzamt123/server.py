document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("data-container");

    function fetchData() {
        fetch("/view")
            .then(response => response.json())
            .then(data => {
                let html = "<ul>";
                data.forEach(item => {
                    html += `<li>Temperatur: ${item.temperature} °C, EC: ${item.ec.toFixed(2)}</li>`;
                });
                html += "</ul>";
                container.innerHTML = html;
            })
            .catch(error => {
                console.error("Fehler beim Abrufen der Daten:", error);
                container.innerHTML = "<p>Fehler beim Laden der Daten.</p>";
            });
    }

    fetchData();
    setInterval(fetchData, 5000); // Alle 5 Sekunden aktualisieren

    document.getElementById("calibrate-btn").addEventListener("click", () => {
        const factor = parseFloat(prompt("Neuen Kalibrierungsfaktor eingeben:"));
        if (!isNaN(factor)) {
            fetch("/calibrate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ factor })
            })
                .then(response => response.text())
                .then(alert)
                .catch(error => console.error("Fehler bei der Kalibrierung:", error));
        }
    });
});
