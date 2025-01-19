document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("data-container");

    // Daten abrufen und anzeigen
    fetch("/view")
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                container.innerHTML = "<p>Keine Daten verfügbar.</p>";
            } else {
                let html = "<ul>";
                data.forEach(item => {
                    html += `<li>${JSON.stringify(item)}</li>`;
                });
                html += "</ul>";
                container.innerHTML = html;
            }
        })
        .catch(error => {
            console.error("Fehler beim Abrufen der Daten:", error);
            container.innerHTML = "<p>Fehler beim Laden der Daten.</p>";
        });
});
