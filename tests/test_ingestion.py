import os
import pytest
import pandas as pd
from src.ingestion import ingest_circuits


def test_returns_dict():
    result = ingest_circuits(["circuit_01"], n_samples=100, output_dir="data/test_tmp")
    assert isinstance(result, dict)


def test_correct_keys():
    ids = ["circuit_01", "circuit_02"]
    result = ingest_circuits(ids, n_samples=100, output_dir="data/test_tmp")
    assert set(result.keys()) == set(ids)


def test_csv_files_created():
    ingest_circuits(["circuit_03"], n_samples=100, output_dir="data/test_tmp")
    files = os.listdir("data/test_tmp")
    assert any("circuit_03" in f for f in files)


def test_dataframe_length():
    result = ingest_circuits(["circuit_04"], n_samples=200, output_dir="data/test_tmp")
    assert len(result["circuit_04"]) == 200


def test_anomaly_circuit():
    result = ingest_circuits(
        ["circuit_05"],
        n_samples=100,
        output_dir="data/test_tmp",
        anomaly_circuits=["circuit_05"],
    )
    assert "circuit_05" in result