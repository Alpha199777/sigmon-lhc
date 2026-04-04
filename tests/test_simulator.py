import pytest
import pandas as pd
from src.simulator import generate_signal


def test_output_is_dataframe():
    df = generate_signal("circuit_01")
    assert isinstance(df, pd.DataFrame)


def test_output_columns():
    df = generate_signal("circuit_01")
    expected = {"timestamp", "circuit_id", "current_A", "voltage_V", "temperature_K"}
    assert expected == set(df.columns)


def test_output_length():
    df = generate_signal("circuit_01", n_samples=500)
    assert len(df) == 500


def test_circuit_id():
    df = generate_signal("circuit_99")
    assert all(df["circuit_id"] == "circuit_99")


def test_anomaly_affects_current():
    df_normal = generate_signal("circuit_01", anomaly=False, noise_level=0)
    df_anomaly = generate_signal("circuit_01", anomaly=True, noise_level=0)
    assert df_anomaly["current_A"].mean() < df_normal["current_A"].mean()


def test_temperature_range():
    df = generate_signal("circuit_01")
    assert df["temperature_K"].between(1.5, 3.0).all()