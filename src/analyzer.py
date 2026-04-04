import numpy as np
import pandas as pd


def compute_statistics(df: pd.DataFrame) -> dict:
    """
    Compute basic statistics for a circuit signal.

    Args:
        df: DataFrame with signal data

    Returns:
        Dictionary of statistical metrics
    """
    return {
        "circuit_id": df["circuit_id"].iloc[0],
        "current_mean": df["current_A"].mean(),
        "current_std": df["current_A"].std(),
        "current_min": df["current_A"].min(),
        "current_max": df["current_A"].max(),
        "voltage_mean": df["voltage_V"].mean(),
        "temperature_mean": df["temperature_K"].mean(),
        "temperature_max": df["temperature_K"].max(),
        "n_samples": len(df),
    }


def detect_anomalies(
    df: pd.DataFrame,
    current_threshold: float = 3.0,
    temperature_limit: float = 2.5,
) -> pd.DataFrame:
    """
    Detect anomalies using z-score and threshold methods.

    Args:
        df: DataFrame with signal data
        current_threshold: Z-score threshold for current anomalies
        temperature_limit: Max acceptable temperature in Kelvin

    Returns:
        DataFrame with anomaly flags
    """
    df = df.copy()
    current_mean = df["current_A"].mean()
    current_std = df["current_A"].std()
    df["current_zscore"] = (df["current_A"] - current_mean) / current_std
    df["anomaly_current"] = df["current_zscore"].abs() > current_threshold
    df["anomaly_temperature"] = df["temperature_K"] > temperature_limit
    df["anomaly"] = df["anomaly_current"] | df["anomaly_temperature"]
    return df


def analyze_circuit(df: pd.DataFrame) -> dict:
    """
    Full analysis pipeline for a single circuit.

    Args:
        df: DataFrame with signal data

    Returns:
        Dictionary with statistics and anomaly summary
    """
    stats = compute_statistics(df)
    df_flagged = detect_anomalies(df)
    n_anomalies = df_flagged["anomaly"].sum()
    anomaly_rate = n_anomalies / len(df_flagged)

    return {
        **stats,
        "n_anomalies": int(n_anomalies),
        "anomaly_rate": round(float(anomaly_rate), 4),
        "status": "CRITICAL" if anomaly_rate > 0.05 else "WARNING" if anomaly_rate > 0.01 else "OK",
    }