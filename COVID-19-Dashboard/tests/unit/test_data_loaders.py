"""Tests for data loaders module"""

import pytest
import pandas as pd
from pathlib import Path

from covid_analytics.data.loaders import DataLoader


class TestDataLoader:
    """Test DataLoader class"""
    
    def test_load_file_not_found(self):
        """Test loading non-existent file"""
        from covid_analytics.core.exceptions import DataLoadError
        
        with pytest.raises(DataLoadError, match="File not found"):
            DataLoader.load("nonexistent.csv")
    
    def test_load_success(self, tmp_path):
        """Test successful data loading"""
        # Create test CSV
        csv_file = tmp_path / "test.csv"
        test_data = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02"],
            "location": ["France", "Germany"],
            "total_cases": [100, 200]
        })
        test_data.to_csv(csv_file, index=False)
        
        # Load
        df = DataLoader.load(csv_file, parse_dates=True, validate=True)
        
        assert len(df) == 2
        assert "date" in df.columns
        assert "location" in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
    
    def test_get_info(self):
        """Test getting dataset info"""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "location": ["France"] * 10,
            "total_cases": range(100, 110)
        })
        
        info = DataLoader.get_info(df)
        
        assert info["rows"] == 10
        assert info["columns"] == 3
        assert "date_range" in info
        assert info["countries"] == 1
        assert "memory_mb" in info
    
    def test_get_info_missing_values(self):
        """Test info with missing values"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02", None],
            "location": ["France", None, "Germany"],
            "total_cases": [100, 200, 300]
        })
        
        info = DataLoader.get_info(df)
        
        assert "missing_values" in info
        assert "date" in info["missing_values"]
        assert "location" in info["missing_values"]
