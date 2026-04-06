---
title: SigMon LHC
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# ⚡ SigMon-LHC — Signal Monitoring & Analysis System

> Inspired by the CERN SigMon project — automated signal analysis for LHC superconducting magnet circuits.

🔴 **Live Dashboard:** [https://doers97-sigmon-lhc.hf.space/dashboard](https://doers97-sigmon-lhc.hf.space/dashboard)

---

## 🎯 Project Overview

Python-based system to process, analyze, and visualize large-scale signal data from LHC superconducting magnet circuits. Detects anomalies in real time using statistical methods and machine learning.

---

## 🏗️ Architecture
---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (Isolation Forest) |
| Frontend | HTML, CSS, JavaScript |
| Node.js Server | Express.js + Morgan |
| CI/CD | GitLab CI/CD |
| Deployment | Hugging Face Spaces (Docker) |
| Notebooks | Jupyter |

---

## 📁 Project Structure

sigmon-lhc/
├── src/
│   ├── simulator.py      # LHC signal simulation (11850A, 1.9K)
│   ├── ingestion.py      # Multi-circuit data pipeline
│   ├── analyzer.py       # Anomaly detection (z-score + threshold)
│   └── api.py            # FastAPI REST endpoints
├── frontend/
│   ├── index.html        # Dashboard UI
│   └── dashboard.js      # JavaScript frontend
├── node-server/
│   └── server.js         # Express.js proxy server
├── notebooks/
│   └── signal_analysis.ipynb  # Jupyter ML analysis
├── tests/                # Pytest unit tests
├── .gitlab-ci.yml        # CI/CD pipeline
└── Dockerfile            # Container for deployment

---

## 🔬 Key Features

- **Signal Simulation** — Realistic LHC values (11,850A current, 1.9K temperature)
- **Anomaly Detection** — Z-score for current outliers + absolute threshold for temperature
- **ML Classification** — Isolation Forest for unsupervised anomaly detection
- **Alert System** — CRITICAL / WARNING / OK circuit classification
- **REST API** — FastAPI with `/ingest` and `/analyze` endpoints
- **Live Dashboard** — Real-time circuit monitoring with color-coded status cards
- **CI/CD Pipeline** — Automated testing on every GitLab push

---

## 🚀 Run Locally
```bash
# Clone and setup
git clone https://github.com/Alpha199777/sigmon-lhc.git
cd sigmon-lhc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start FastAPI
python -m uvicorn src.api:app --reload

# Open dashboard
http://127.0.0.1:8000/dashboard
```

---

## ✅ Test Suite
```bash
python -m pytest tests/ -v
```

| Test File | Coverage |
|-----------|----------|
| test_simulator.py | Signal generation, anomaly injection |
| test_ingestion.py | CSV export, multi-circuit pipeline |
| test_analyzer.py | Z-score detection, status classification |

---

## 👤 Author

**Junior** — I 
Portfolio project demonstrating: Python · FastAPI · GitLab CI/CD · ML · JavaScript · Node.js · Docker