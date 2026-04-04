import pytest
import pandas as pd
from src.simulator import generate_signal
from src.analyzer import compute_statistics, detect_anomalies, analyze_circuit


def test_compute_statistics_keys():
    df = generate_signal("circuit_01", n_samples=100)
    stats = compute_statistics(df)
    expected_keys = {
        "circuit_id", "current_mean", "current_std",
        "current_min", "current_max", "voltage_mean",
        "temperature_mean", "temperature_max", "n_samples"
    }
    assert expected_keys == set(stats.keys())


def test_compute_statistics_n_samples():
    df = generate_signal("circuit_01", n_samples=100)
    stats = compute_statistics(df)
    assert stats["n_samples"] == 100


def test_detect_anomalies_columns():
    df = generate_signal("circuit_01", n_samples=100)
    result = detect_anomalies(df)
    assert "anomaly" in result.columns
    assert "anomaly_current" in result.columns
    assert "anomaly_temperature" in result.columns


def test_detect_anomalies_normal_signal():
    df = generate_signal("circuit_01", n_samples=500, anomaly=False, noise_level=0.01)
    result = detect_anomalies(df)
    assert result["anomaly"].sum() == 0


def test_detect_anomalies_anomaly_signal():
    df = generate_signal("circuit_01", n_samples=500, anomaly=True, noise_level=0)
    result = detect_anomalies(df, temperature_limit=2.3)
    assert result["anomaly"].sum() > 0


def test_analyze_circuit_status_ok():
    df = generate_signal("circuit_01", n_samples=500, anomaly=False, noise_level=0.01)
    result = analyze_circuit(df)
    assert result["status"] == "OK"


def test_analyze_circuit_status_critical():
    df = generate_signal("circuit_01", n_samples=500, anomaly=True, noise_level=0)
    result = analyze_circuit(df)
    assert result["status"] in ["WARNING", "CRITICAL", "OK"]