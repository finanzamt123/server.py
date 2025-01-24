document.addEventListener("DOMContentLoaded", () => {
    const ecValue = document.getElementById("ec-value");
    const waterTemp = document.getElementById("water-temp");
    const airTemp = document.getElementById("air-temp");
    const ecGraph = document.getElementById("ec-graph").getContext("2d");

    let ecChart;

    // Fetch initial data
    async function fetchData() {
        const response = await fetch("/");
        const { current_values, schedules } = await response.json();

        ecValue.textContent = current_values.ec.toFixed(2);
        waterTemp.textContent = current_values.water_temp.toFixed(1);
        airTemp.textContent = current_values.air_temp.toFixed(1);

        updateScheduleTable("watering-schedule", schedules.watering);
        updateScheduleTable("ec-correction-schedule", schedules.ec_correction);

        fetchGraphData();
    }

    // Update schedule table
    function updateScheduleTable(tableId, schedule) {
        const tbody = document.getElementById(tableId).querySelector("tbody");
        tbody.innerHTML = "";
        schedule.forEach((entry, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.time}</td>
                <td>${entry.duration}</td>
                <td>
                    <button class="delete-btn" data-index="${index}" data-table="${tableId}">Löschen</button>
                </td>`;
            tbody.appendChild(row);
        });
    }

    // Fetch and render graph data
    async function fetchGraphData() {
        const response = await fetch("/ec_data");
        const data = await response.json();

        if (!ecChart) {
            ecChart = new Chart(ecGraph, {
                type: "line",
                data: {
                    labels: data.timestamps,
                    datasets: [{
                        label: "EC-Wert (µS/cm)",
                        data: data.values,
                        borderColor: "blue",
                        fill: false
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
        } else {
            ecChart.data.labels = data.timestamps;
            ecChart.data.datasets[0].data = data.values;
            ecChart.update();
        }
    }

    fetchData();

    // Auto-update every 60 seconds
    setInterval(fetchData, 60000);
});
