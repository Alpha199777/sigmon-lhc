import os
import pandas as pd
from datetime import datetime
from src.simulator import generate_signal


def ingest_circuits(
    circuit_ids: list,
    n_samples: int = 1000,
    output_dir: str = "data/raw",
    anomaly_circuits: list = None,
) -> dict:
    """
    Generate and store signal data for multiple circuits.

    Args:
        circuit_ids: List of circuit identifiers
        n_samples: Number of samples per circuit
        output_dir: Directory to save CSV files
        anomaly_circuits: List of circuit IDs to inject anomalies

    Returns:
        Dictionary mapping circuit_id to DataFrame
    """
    os.makedirs(output_dir, exist_ok=True)
    anomaly_circuits = anomaly_circuits or []
    results = {}

    for circuit_id in circuit_ids:
        anomaly = circuit_id in anomaly_circuits
        df = generate_signal(
            circuit_id=circuit_id,
            n_samples=n_samples,
            anomaly=anomaly,
        )
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{circuit_id}_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        results[circuit_id] = df
        print(f"✅ Saved: {filepath}")

    return results