document.addEventListener("DOMContentLoaded", () => {
    updateCurrentValues();
    loadSchedules();
    loadGraph();
});

function updateCurrentValues() {
    fetch("/current_values")
        .then(response => response.json())
        .then(data => {
            document.getElementById("ec_value").textContent = data.ec;
            document.getElementById("water_temp").textContent = data.water_temp;
            document.getElementById("air_temp").textContent = data.air_temp;
        });
}

function loadSchedules() {
    // Implement loading and rendering of schedules
}

function loadGraph() {
    fetch("/ec_graph_data")
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("ec_graph").getContext("2d");
            const labels = data.map(entry => entry.timestamp);
            const values = data.map(entry => entry.ec_value);
            new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "EC Value (µS)",
                        data: values,
                        borderColor: "blue",
                        fill: false
                    }]
                }
            });
        });
}
