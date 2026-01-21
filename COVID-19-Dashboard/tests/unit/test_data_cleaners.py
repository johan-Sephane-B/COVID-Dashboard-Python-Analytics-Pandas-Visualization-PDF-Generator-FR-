"""Tests for data cleaners module"""

import pytest
import pandas as pd
import numpy as np

from covid_analytics.processing.cleaners import DataCleaner


class TestDataCleaner:
    """Test DataCleaner class"""
    
    def test_remove_duplicates(self):
        """Test duplicate removal"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-01", "2020-01-02"],
            "location": ["France", "France", "France"],
            "total_cases": [100, 100, 150]
        })
        
        cleaner = DataCleaner()
        df_clean = cleaner._remove_duplicates(df)
        
        assert len(df_clean) == 2  # One duplicate removed
    
    def test_fix_data_types(self):
        """Test data type conversion"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02"],
            "location": ["France", "Germany"],
            "total_cases": ["100", "200"],  # String numbers
            "total_deaths": ["10", "20"]
        })
        
        cleaner = DataCleaner()
        df_typed = cleaner._fix_data_types(df)
        
        assert pd.api.types.is_datetime64_any_dtype(df_typed["date"])
        assert pd.api.types.is_numeric_dtype(df_typed["total_cases"])
        assert pd.api.types.is_numeric_dtype(df_typed["total_deaths"])
    
    def test_validate_negative_values(self):
        """Test negative value correction"""
        df = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=3),
            "location": ["France"] * 3,
            "total_cases": [100, -50, 200],  # Negative value
            "total_deaths": [10, 5, -3]  # Negative value
        })
        
        cleaner = DataCleaner()
        df_valid = cleaner._validate_values(df)
        
        assert (df_valid["total_cases"] >= 0).all()
        assert (df_valid["total_deaths"] >= 0).all()
    
    def test_sort_data(self):
        """Test data sorting"""
        df = pd.DataFrame({
            "date": ["2020-01-02", "2020-01-01", "2020-01-03"],
            "location": ["France", "France", "France"],
            "total_cases": [150, 100, 200]
        })
        df["date"] = pd.to_datetime(df["date"])
        
        cleaner = DataCleaner()
        df_sorted = cleaner._sort_data(df)
        
        assert df_sorted["date"].is_monotonic_increasing
    
    def test_full_pipeline(self):
        """Test complete cleaning pipeline"""
        df = pd.DataFrame({
            "date": ["2020-01-02", "2020-01-01", "2020-01-01"],
            "location": ["France", "France", "France"],
            "total_cases": ["150", "100", "100"],
            "total_deaths": ["15", "-5", "10"]
        })
        
        cleaner = DataCleaner()
        df_clean = cleaner.clean(df)
        
        # Check results
        assert len(df_clean) == 2  # Duplicate removed
        assert pd.api.types.is_datetime64_any_dtype(df_clean["date"])
        assert (df_clean["total_deaths"] >= 0).all()
        assert df_clean["date"].is_monotonic_increasing
