const express = require("express");
const morgan = require("morgan");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();
const PORT = 3000;
const FASTAPI_URL = "http://127.0.0.1:8000";

app.use(morgan("combined"));
app.use(express.json());

app.get("/node/health", (req, res) => {
    res.json({
        status: "ok",
        service: "SigMon-LHC Node.js Server",
        version: "1.0.0",
        fastapi_url: FASTAPI_URL,
        timestamp: new Date().toISOString()
    });
});

app.get("/node/circuits/summary", async (req, res) => {
    try {
        const response = await fetch(FASTAPI_URL + "/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                circuit_ids: ["circuit_01", "circuit_02", "circuit_03", "circuit_04", "circuit_05", "circuit_06", "circuit_07"],
                n_samples: 500,
                anomaly_circuits: []
            })
        });
        const data = await response.json();
        const results = data.results;
        const summary = {
            total: Object.keys(results).length,
            ok: Object.values(results).filter(r => r.status === "OK").length,
            warning: Object.values(results).filter(r => r.status === "WARNING").length,
            critical: Object.values(results).filter(r => r.status === "CRITICAL").length,
            circuits: results
        };
        res.json(summary);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.use("/", createProxyMiddleware({
    target: FASTAPI_URL,
    changeOrigin: true,
    on: {
        error: (err, req, res) => {
            res.status(502).json({ error: "FastAPI unreachable", detail: err.message });
        }
    }
}));

app.listen(PORT, () => {
    console.log("SigMon-LHC Node.js server running on http://127.0.0.1:" + PORT);
    console.log("Proxying requests to FastAPI at " + FASTAPI_URL);
});