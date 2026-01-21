"""Pytest configuration and fixtures"""

import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_covid_data():
    """Sample COVID-19 data for testing"""
    return pd.DataFrame({
        "date": pd.date_range("2020-01-01", periods=10),
        "location": ["France"] * 5 + ["Germany"] * 5,
        "total_cases": [100, 150, 200, 250, 300, 50, 75, 100, 125, 150],
        "total_deaths": [10, 15, 20, 25, 30, 5, 7, 10, 12, 15],
        "new_cases": [100, 50, 50, 50, 50, 50, 25, 25, 25, 25],
        "new_deaths": [10, 5, 5, 5, 5, 5, 2, 3, 2, 3],
    })


@pytest.fixture
def sample_csv_file(tmp_path, sample_covid_data):
    """Create a temporary CSV file with sample data"""
    csv_file = tmp_path / "test_data.csv"
    sample_covid_data.to_csv(csv_file, index=False)
    return csv_file
