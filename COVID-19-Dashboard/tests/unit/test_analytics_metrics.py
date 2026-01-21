"""Tests for metrics calculator"""

import pytest
import pandas as pd
import numpy as np

from covid_analytics.analytics.metrics import MetricsCalculator


class TestMetricsCalculator:
    """Test MetricsCalculator class"""
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=10),
            "location": ["France"] * 10,
            "total_cases": [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
            "total_deaths": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
            "new_cases": [100, 50, 50, 50, 50, 50, 50, 50, 50, 50],
            "new_deaths": [10, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            "population": [67000000] * 10
        })
    
    def test_initialization(self, sample_data):
        """Test calculator initialization"""
        calc = MetricsCalculator(sample_data)
        assert calc.data is not None
        assert len(calc.data) == 10
    
    def test_mortality_rate(self, sample_data):
        """Test mortality rate calculation"""
        calc = MetricsCalculator(sample_data)
        rate = calc.mortality_rate(country="France")
        
        # Expected: 55/550 * 100 = 10%
        assert 9.0 < rate < 11.0
    
    def test_mortality_rate_no_country(self, sample_data):
        """Test mortality rate without country filter"""
        calc = MetricsCalculator(sample_data)
        rate = calc.mortality_rate()
        
        assert rate > 0
    
    def test_case_fatality_rate(self, sample_data):
        """Test CFR calculation"""
        calc = MetricsCalculator(sample_data)
        cfr = calc.case_fatality_rate(country="France")
        
        # Expected: 50/500 * 100 = 10%
        assert 9.0 < cfr < 11.0
    
    def test_growth_rate(self, sample_data):
        """Test growth rate calculation"""
        calc = MetricsCalculator(sample_data)
        growth = calc.growth_rate(metric="total_cases", country="France", window=1)
        
        assert isinstance(growth, pd.Series)
        assert len(growth) == 10
    
    def test_daily_average(self, sample_data):
        """Test rolling average"""
        calc = MetricsCalculator(sample_data)
        avg = calc.daily_average(metric="new_cases", country="France", window=3)
        
        assert isinstance(avg, pd.Series)
        assert len(avg) == 10
    
    def test_total_by_country(self, sample_data):
        """Test totals by country"""
        calc = MetricsCalculator(sample_data)
        totals = calc.total_by_country(metric="total_cases")
        
        assert isinstance(totals, pd.DataFrame)
        assert "France" in totals.index
    
    def test_compare_countries(self):
        """Test country comparison"""
        data = pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=6),
            "location": ["France", "France", "France", "Germany", "Germany", "Germany"],
            "total_cases": [100, 200, 300, 150, 250, 350],
            "population": [67000000, 67000000, 67000000, 83000000, 83000000, 83000000]
        })
        
        calc = MetricsCalculator(data)
        comparison = calc.compare_countries(
            countries=["France", "Germany"],
            metric="total_cases"
        )
        
        assert isinstance(comparison, pd.DataFrame)
        assert "France" in comparison.columns
        assert "Germany" in comparison.columns
    
    def test_missing_columns(self):
        """Test error handling for missing columns"""
        data = pd.DataFrame({
            "date": ["2020-01-01"],
            "location": ["France"]
        })
        
        calc = MetricsCalculator(data)
        rate = calc.mortality_rate()
        
        # Should return 0 when columns are missing
        assert rate == 0.0
