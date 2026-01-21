"""
Tests for metrics calculation module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src_new to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src_new"))

from epi_analytics.metrics import (
    analyze,
    _calculate_mortality,
    _calculate_growth_rate,
    _detect_peaks,
    _compare_countries,
    calculate_doubling_time,
    calculate_r_number
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range('2020-01-01', periods=30, freq='D')
    data = pd.DataFrame({
        'location': ['France'] * 30,
        'date': dates,
        'total_cases': np.cumsum(np.random.randint(10, 100, 30)),
        'total_deaths': np.cumsum(np.random.randint(0, 10, 30)),
        'new_cases': np.random.randint(10, 100, 30),
        'new_deaths': np.random.randint(0, 10, 30),
        'population': [67000000] * 30
    })
    return data


@pytest.fixture
def multi_country_data():
    """Create multi-country data for testing."""
    countries = ['France', 'Germany', 'Italy']
    dates = pd.date_range('2020-01-01', periods=10, freq='D')
    
    data_list = []
    for country in countries:
        for date in dates:
            data_list.append({
                'location': country,
                'date': date,
                'total_cases': np.random.randint(1000, 10000),
                'total_deaths': np.random.randint(10, 500),
                'population': 60000000
            })
    
    return pd.DataFrame(data_list)


class TestAnalyzeFunction:
    """Test the main analyze function."""
    
    def test_analyze_mortality(self, sample_data):
        """Test mortality calculation via analyze."""
        result = analyze(sample_data, metric="mortality")
        
        assert isinstance(result, float)
        assert 0 <= result <= 100  # Percentage
    
    def test_analyze_growth(self, sample_data):
        """Test growth rate calculation via analyze."""
        result = analyze(sample_data, metric="growth")
        
        assert isinstance(result, float)
    
    def test_analyze_with_country_filter(self, multi_country_data):
        """Test analyze with country filtering."""
        result = analyze(multi_country_data, metric="mortality", country="France")
        
        assert isinstance(result, float)
    
    def test_analyze_compare(self, multi_country_data):
        """Test country comparison via analyze."""
        result = analyze(
            multi_country_data,
            metric="compare",
            countries=["France", "Germany"]
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
    
    def test_analyze_invalid_metric_raises_error(self, sample_data):
        """Test that invalid metric raises ValueError."""
        with pytest.raises(ValueError, match="Unknown metric"):
            analyze(sample_data, metric="invalid_metric")


class TestMortalityCalculation:
    """Test mortality rate calculations."""
    
    def test_calculate_mortality_cumulative(self, sample_data):
        """Test cumulative mortality calculation."""
        mortality = _calculate_mortality(sample_data, method="cumulative")
        
        assert isinstance(mortality, float)
        assert mortality >= 0
    
    def test_calculate_mortality_daily(self, sample_data):
        """Test daily mortality calculation."""
        mortality = _calculate_mortality(sample_data, method="daily")
        
        assert isinstance(mortality, float)
        assert mortality >= 0
    
    def test_calculate_mortality_zero_cases(self):
        """Test mortality with zero cases."""
        data = pd.DataFrame({
            'total_cases': [0],
            'total_deaths': [0]
        })
        
        mortality = _calculate_mortality(data)
        assert mortality == 0.0
    
    def test_calculate_mortality_invalid_method(self, sample_data):
        """Test that invalid method raises error."""
        with pytest.raises(ValueError, match="Unknown method"):
            _calculate_mortality(sample_data, method="invalid")


class TestGrowthRateCalculation:
    """Test growth rate calculations."""
    
    def test_calculate_growth_rate(self, sample_data):
        """Test growth rate calculation."""
        growth = _calculate_growth_rate(sample_data, metric_col="total_cases")
        
        assert isinstance(growth, float)
    
    def test_calculate_growth_rate_with_window(self, sample_data):
        """Test growth rate with custom window."""
        growth = _calculate_growth_rate(sample_data, metric_col="total_cases", window=14)
        
        assert isinstance(growth, float)
    
    def test_calculate_growth_rate_invalid_column(self, sample_data):
        """Test that invalid column raises error."""
        with pytest.raises(ValueError, match="not found"):
            _calculate_growth_rate(sample_data, metric_col="nonexistent_column")


class TestPeakDetection:
    """Test peak detection."""
    
    def test_detect_peaks_returns_dataframe(self, sample_data):
        """Test that peak detection returns DataFrame."""
        peaks = _detect_peaks(sample_data, metric_col="new_cases")
        
        assert isinstance(peaks, pd.DataFrame)
        assert 'date' in peaks.columns
        assert 'peak_value' in peaks.columns
    
    def test_detect_peaks_with_prominence(self, sample_data):
        """Test peak detection with custom prominence."""
        peaks = _detect_peaks(sample_data, metric_col="new_cases", prominence=0.2)
        
        assert isinstance(peaks, pd.DataFrame)
    
    def test_detect_peaks_invalid_column(self, sample_data):
        """Test that invalid column raises error."""
        with pytest.raises(ValueError, match="not found"):
            _detect_peaks(sample_data, metric_col="nonexistent_column")


class TestCountryComparison:
    """Test country comparison."""
    
    def test_compare_countries(self, multi_country_data):
        """Test basic country comparison."""
        comparison = _compare_countries(multi_country_data, metric_col="total_cases")
        
        assert isinstance(comparison, pd.DataFrame)
        assert 'location' in comparison.columns
        assert 'total_cases' in comparison.columns
    
    def test_compare_countries_sorted(self, multi_country_data):
        """Test that comparison is sorted by metric."""
        comparison = _compare_countries(multi_country_data, metric_col="total_cases")
        
        # Should be sorted descending
        assert comparison['total_cases'].is_monotonic_decreasing
    
    def test_compare_countries_with_normalization(self, multi_country_data):
        """Test comparison with population normalization."""
        comparison = _compare_countries(
            multi_country_data,
            metric_col="total_cases",
            normalize=True
        )
        
        assert 'total_cases_per_million' in comparison.columns


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_calculate_doubling_time(self, sample_data):
        """Test doubling time calculation."""
        doubling = calculate_doubling_time(sample_data, metric_col="total_cases")
        
        assert isinstance(doubling, float)
        assert doubling > 0
    
    def test_calculate_r_number(self, sample_data):
        """Test R number calculation."""
        r = calculate_r_number(sample_data, generation_time=5)
        
        assert isinstance(r, float)
        assert r >= 0


# Integration tests
class TestMetricsIntegration:
    """Integration tests for metrics module."""
    
    def test_full_analysis_workflow(self, multi_country_data):
        """Test complete analysis workflow."""
        # Calculate multiple metrics
        mortality = analyze(multi_country_data, metric="mortality", country="France")
        growth = analyze(multi_country_data, metric="growth", country="France")
        comparison = analyze(
            multi_country_data,
            metric="compare",
            countries=["France", "Germany", "Italy"]
        )
        
        assert isinstance(mortality, float)
        assert isinstance(growth, float)
        assert isinstance(comparison, pd.DataFrame)
        assert len(comparison) == 3
