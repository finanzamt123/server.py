document.addEventListener("DOMContentLoaded", () => {
    const temperatureSpan = document.getElementById("temperature");
    const ecSpan = document.getElementById("ec");

    function fetchData() {
        fetch("/view") // Ruft die Daten vom Server ab
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
});
