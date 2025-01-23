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
