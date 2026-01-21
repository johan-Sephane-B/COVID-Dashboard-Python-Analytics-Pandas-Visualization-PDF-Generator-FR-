"""Tests for data sources module"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

from covid_analytics.data.sources import DataSource, _parse_interval


class TestDataSource:
    """Test DataSource class"""
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        df = DataSource.synthetic(countries=3, days=10, seed=42)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 30  # 3 countries × 10 days
        assert "date" in df.columns
        assert "location" in df.columns
        assert "total_cases" in df.columns
        assert "total_deaths" in df.columns
        
        # Check data types
        assert df["total_cases"].dtype in [int, float]
        assert df["total_deaths"].dtype in [int, float]
    
    def test_synthetic_data_reproducibility(self):
        """Test that synthetic data is reproducible with same seed"""
        df1 = DataSource.synthetic(countries=2, days=5, seed=42)
        df2 = DataSource.synthetic(countries=2, days=5, seed=42)
        
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_from_csv_file_not_found(self):
        """Test loading from non-existent CSV"""
        from covid_analytics.core.exceptions import DataLoadError
        
        with pytest.raises(DataLoadError, match="File not found"):
            DataSource.from_csv("nonexistent.csv")
    
    def test_from_csv_success(self, tmp_path):
        """Test successful CSV loading"""
        # Create temporary CSV
        csv_file = tmp_path / "test_data.csv"
        test_data = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02"],
            "location": ["France", "France"],
            "total_cases": [100, 150]
        })
        test_data.to_csv(csv_file, index=False)
        
        # Load and verify
        df = DataSource.from_csv(csv_file)
        assert len(df) == 2
        assert "date" in df.columns
        assert "location" in df.columns


class TestParseInterval:
    """Test interval parsing helper"""
    
    def test_parse_hours(self):
        """Test parsing hour intervals"""
        assert _parse_interval("12h") == 12
        assert _parse_interval("24h") == 24
    
    def test_parse_days(self):
        """Test parsing day intervals"""
        assert _parse_interval("1d") == 24
        assert _parse_interval("7d") == 168
    
    def test_parse_invalid(self):
        """Test invalid interval defaults to 24h"""
        assert _parse_interval("invalid") == 24
        assert _parse_interval("") == 24
