"""Integration tests for covid-analytics library"""

import pytest
import pandas as pd

from covid_analytics.data.sources import DataSource
from covid_analytics.processing.cleaners import DataCleaner
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector


class TestEndToEnd:
    """End-to-end integration tests"""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing"""
        return DataSource.synthetic(countries=3, days=30, seed=42)
    
    def test_complete_workflow(self, sample_data):
        """Test complete workflow: load → clean → analyze"""
        # 1. Data should be loaded
        assert len(sample_data) > 0
        assert 'date' in sample_data.columns
        assert 'location' in sample_data.columns
        
        # 2. Clean data
        cleaner = DataCleaner()
        clean_data = cleaner.clean(sample_data)
        
        assert len(clean_data) > 0
        assert len(clean_data) <= len(sample_data)
        
        # 3. Calculate metrics
        metrics = MetricsCalculator(clean_data)
        country = clean_data['location'].iloc[0]
        
        mortality = metrics.mortality_rate(country=country)
        assert isinstance(mortality, float)
        assert mortality >= 0
        
        # 4. Detect trends
        detector = TrendDetector(clean_data)
        summary = detector.get_trend_summary(metric="total_cases", country=country)
        
        assert 'trend' in summary
        assert summary['trend'] in ['increasing', 'decreasing', 'stable', 'unknown']
    
    def test_multi_country_analysis(self, sample_data):
        """Test analysis across multiple countries"""
        cleaner = DataCleaner()
        clean_data = cleaner.clean(sample_data)
        
        metrics = MetricsCalculator(clean_data)
        countries = clean_data['location'].unique()
        
        results = []
        for country in countries:
            mortality = metrics.mortality_rate(country=country)
            results.append({
                'country': country,
                'mortality': mortality
            })
        
        assert len(results) == len(countries)
        assert all(r['mortality'] >= 0 for r in results)
    
    def test_data_quality_after_cleaning(self, sample_data):
        """Test that cleaned data meets quality standards"""
        cleaner = DataCleaner()
        clean_data = cleaner.clean(sample_data)
        
        # No duplicates
        assert not clean_data.duplicated(subset=['date', 'location']).any()
        
        # Dates are sorted
        for country in clean_data['location'].unique():
            country_data = clean_data[clean_data['location'] == country]
            dates = pd.to_datetime(country_data['date'])
            assert dates.is_monotonic_increasing
        
        # No negative values in cumulative columns
        if 'total_cases' in clean_data.columns:
            assert (clean_data['total_cases'] >= 0).all()
        if 'total_deaths' in clean_data.columns:
            assert (clean_data['total_deaths'] >= 0).all()
    
    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        data = DataSource.synthetic(countries=1, days=10)
        cleaner = DataCleaner()
        clean_data = cleaner.clean(data)
        
        metrics = MetricsCalculator(clean_data)
        
        # Invalid country should not crash
        mortality = metrics.mortality_rate(country="NonExistentCountry")
        assert mortality == 0.0  # Should return 0 for missing country
    
    def test_performance_acceptable(self, sample_data):
        """Test that performance is acceptable"""
        import time
        
        # Cleaning should be fast
        cleaner = DataCleaner()
        start = time.time()
        clean_data = cleaner.clean(sample_data)
        clean_time = time.time() - start
        
        assert clean_time < 1.0  # Should clean in < 1 second
        
        # Analytics should be fast
        metrics = MetricsCalculator(clean_data)
        country = clean_data['location'].iloc[0]
        
        start = time.time()
        _ = metrics.mortality_rate(country=country)
        analytics_time = time.time() - start
        
        assert analytics_time < 0.1  # Should calculate in < 100ms
