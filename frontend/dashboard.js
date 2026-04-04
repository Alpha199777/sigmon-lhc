const API_URL = "";

async function analyzeCircuits() {
    console.log("Analyze clicked");
    const samples = parseInt(document.getElementById("samples-input").value);
    const statusMsg = document.getElementById("status-msg");
    const selectEl = document.getElementById("circuit-input");
    const circuitIds = Array.from(selectEl.selectedOptions).map(function(o) { return o.value; });

    if (circuitIds.length === 0) {
        statusMsg.textContent = "Please select at least one circuit.";
        return;
    }
    statusMsg.textContent = "Analyzing circuits...";
    try {
        const response = await fetch(API_URL + "/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ circuit_ids: circuitIds, n_samples: samples, anomaly_circuits: [] })
        });
        if (!response.ok) throw new Error("API error: " + response.status);
        const data = await response.json();
        console.log("Data received:", data);
        renderDashboard(data.results);
        statusMsg.textContent = "Analysis complete - " + circuitIds.length + " circuit(s) analyzed.";
    } catch (error) {
        console.error("Error:", error);
        statusMsg.textContent = "Error: " + error.message;
    }
}

function renderDashboard(results) {
    const grid = document.getElementById("grid");
    const summary = document.getElementById("summary");
    grid.innerHTML = "";
    let nOk = 0, nWarning = 0, nCritical = 0;

    for (const circuitId in results) {
        const result = results[circuitId];
        const status = result.status.toLowerCase();
        if (status === "ok") nOk++;
        else if (status === "warning") nWarning++;
        else nCritical++;

        const card = document.createElement("div");
        card.className = "card " + status;
        card.innerHTML =
            "<div class='card-header'>" +
            "<span class='card-title'>" + circuitId + "</span>" +
            "<span class='badge " + status + "'>" + result.status + "</span>" +
            "</div>" +
            "<div class='metric'><span class='metric-label'>Current Mean</span><span class='metric-value'>" + result.current_mean.toFixed(2) + " A</span></div>" +
            "<div class='metric'><span class='metric-label'>Current Std</span><span class='metric-value'>" + result.current_std.toFixed(2) + " A</span></div>" +
            "<div class='metric'><span class='metric-label'>Temp Max</span><span class='metric-value'>" + result.temperature_max.toFixed(3) + " K</span></div>" +
            "<div class='metric'><span class='metric-label'>Anomalies</span><span class='metric-value'>" + result.n_anomalies + "</span></div>" +
            "<div class='metric'><span class='metric-label'>Anomaly Rate</span><span class='metric-value'>" + (result.anomaly_rate * 100).toFixed(2) + "%</span></div>";
        grid.appendChild(card);
    }

    summary.innerHTML =
        "<div class='stat-box'><div class='number ok-color'>" + nOk + "</div><div class='label'>OK</div></div>" +
        "<div class='stat-box'><div class='number warning-color'>" + nWarning + "</div><div class='label'>WARNING</div></div>" +
        "<div class='stat-box'><div class='number critical-color'>" + nCritical + "</div><div class='label'>CRITICAL</div></div>" +
        "<div class='stat-box'><div class='number'>" + (nOk + nWarning + nCritical) + "</div><div class='label'>TOTAL</div></div>";
}

function clearDashboard() {
    document.getElementById("grid").innerHTML = "";
    document.getElementById("summary").innerHTML = "";
    document.getElementById("status-msg").textContent = "Dashboard cleared.";
}

document.getElementById("btn-analyze").addEventListener("click", analyzeCircuits);
document.getElementById("btn-clear").addEventListener("click", clearDashboard);