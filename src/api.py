from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from src.ingestion import ingest_circuits
from src.analyzer import analyze_circuit

app = FastAPI(
    title="SigMon-LHC API",
    description="Signal Monitoring & Analysis System for LHC magnet circuits",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/index.html")

class IngestionRequest(BaseModel):
    circuit_ids: List[str]
    n_samples: int = 1000
    anomaly_circuits: Optional[List[str]] = []


class AnalysisRequest(BaseModel):
    circuit_ids: List[str]
    n_samples: int = 1000
    anomaly_circuits: Optional[List[str]] = []


@app.get("/")
def root():
    return {"message": "SigMon-LHC API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest")
def ingest(request: IngestionRequest):
    try:
        results = ingest_circuits(
            circuit_ids=request.circuit_ids,
            n_samples=request.n_samples,
            anomaly_circuits=request.anomaly_circuits,
        )
        return {
            "status": "success",
            "circuits_ingested": list(results.keys()),
            "n_samples": request.n_samples,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
def analyze(request: AnalysisRequest):
    try:
        results = ingest_circuits(
            circuit_ids=request.circuit_ids,
            n_samples=request.n_samples,
            anomaly_circuits=request.anomaly_circuits,
        )
        analysis = {}
        for circuit_id, df in results.items():
            analysis[circuit_id] = analyze_circuit(df)
        return {
            "status": "success",
            "results": analysis,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))