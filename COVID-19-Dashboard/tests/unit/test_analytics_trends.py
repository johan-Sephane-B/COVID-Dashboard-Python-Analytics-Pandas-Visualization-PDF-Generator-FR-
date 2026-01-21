"""Tests for trend detector"""

import pytest
import pandas as pd
import numpy as np

from covid_analytics.analytics.trends import TrendDetector, TrendDirection


class TestTrendDetector:
    """Test TrendDetector class"""
    
    @pytest.fixture
    def sample_data(self):
        """Sample data with trends"""
        return pd.DataFrame({
            "date": pd.date_range("2020-01-01", periods=20),
            "location": ["France"] * 20,
            "total_cases": [
                100, 120, 150, 180, 220, 270, 330, 400, 480, 570,  # Increasing
                660, 750, 840, 920, 990, 1050, 1100, 1140, 1170, 1190  # Slowing
            ]
        })
    
    def test_initialization(self, sample_data):
        """Test detector initialization"""
        detector = TrendDetector(sample_data)
        assert detector.data is not None
        assert len(detector.data) == 20
    
    def test_detect_trends(self, sample_data):
        """Test trend detection"""
        detector = TrendDetector(sample_data)
        trends = detector.detect(
            metric="total_cases",
            country="France",
            window=3,
            threshold=0.1
        )
        
        assert isinstance(trends, pd.DataFrame)
        assert "trend" in trends.columns
        assert "rolling_avg" in trends.columns
        assert "pct_change" in trends.columns
    
    def test_trend_classification(self, sample_data):
        """Test trend classification"""
        detector = TrendDetector(sample_data)
        
        # Test increasing trend
        assert detector._classify_trend(0.15, 0.1) == TrendDirection.INCREASING
        
        # Test decreasing trend
        assert detector._classify_trend(-0.15, 0.1) == TrendDirection.DECREASING
        
        # Test stable trend
        assert detector._classify_trend(0.05, 0.1) == TrendDirection.STABLE
        
        # Test unknown (NaN)
        assert detector._classify_trend(np.nan, 0.1) == TrendDirection.UNKNOWN
    
    def test_get_trend_summary(self, sample_data):
        """Test trend summary"""
        detector = TrendDetector(sample_data)
        summary = detector.get_trend_summary(
            metric="total_cases",
            country="France",
            window=3
        )
        
        assert isinstance(summary, dict)
        assert "trend" in summary
        assert "change" in summary
        assert "current_value" in summary
        assert "rolling_avg" in summary
        assert "date" in summary
    
    def test_detect_anomalies(self, sample_data):
        """Test anomaly detection"""
        # Add an anomaly
        sample_data.loc[10, "total_cases"] = 10000  # Huge spike
        
        detector = TrendDetector(sample_data)
        anomalies = detector.detect_anomalies(
            metric="total_cases",
            country="France",
            std_threshold=2.0
        )
        
        assert isinstance(anomalies, pd.DataFrame)
        assert len(anomalies) > 0
        assert "z_score" in anomalies.columns
    
    def test_missing_date_column(self):
        """Test error handling for missing date column"""
        data = pd.DataFrame({
            "location": ["France"],
            "total_cases": [100]
        })
        
        with pytest.raises(ValueError, match="must have 'date' column"):
            TrendDetector(data)
    
    def test_missing_metric(self, sample_data):
        """Test error handling for missing metric"""
        detector = TrendDetector(sample_data)
        
        with pytest.raises(ValueError, match="not found"):
            detector.detect(metric="nonexistent_metric")
