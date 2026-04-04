import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_signal(
    circuit_id: str,
    n_samples: int = 1000,
    sampling_rate: float = 100.0,
    noise_level: float = 0.05,
    anomaly: bool = False,
) -> pd.DataFrame:
    """
    Simulate LHC magnet circuit signal data.

    Args:
        circuit_id: Unique circuit identifier
        n_samples: Number of data points
        sampling_rate: Hz
        noise_level: Gaussian noise amplitude
        anomaly: Inject anomaly if True

    Returns:
        DataFrame with timestamp, current, voltage, temperature
    """
    t = np.linspace(0, n_samples / sampling_rate, n_samples)
    current = 11850 + 50 * np.sin(2 * np.pi * 0.1 * t) + noise_level * np.random.randn(n_samples)
    voltage = 0.1 * current + noise_level * np.random.randn(n_samples)
    temperature = 1.9 + 0.01 * np.sin(2 * np.pi * 0.05 * t) + noise_level * 0.1 * np.random.randn(n_samples)

    if anomaly:
        anomaly_idx = np.random.randint(n_samples // 2, n_samples)
        current[anomaly_idx:] *= 0.6
        temperature[anomaly_idx:] += 0.5

    timestamps = [datetime(2024, 1, 1) + timedelta(seconds=float(t[i])) for i in range(n_samples)]

    return pd.DataFrame({
        "timestamp": timestamps,
        "circuit_id": circuit_id,
        "current_A": current,
        "voltage_V": voltage,
        "temperature_K": temperature,
    })