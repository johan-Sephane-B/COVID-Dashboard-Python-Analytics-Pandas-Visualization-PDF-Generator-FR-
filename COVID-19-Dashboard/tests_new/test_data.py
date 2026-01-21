"""
Tests for data loading module.
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add src_new to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src_new"))

from epi_analytics.data import (
    load_data,
    _download_owid,
    _load_from_cache,
    _load_sample,
    _clean_data
)


class TestLoadData:
    """Test the main load_data function."""
    
    def test_load_data_returns_dataframe(self):
        """Test that load_data returns a DataFrame."""
        # This will use sample data if download fails
        data = load_data()
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
    
    def test_load_data_has_required_columns(self):
        """Test that loaded data has essential columns."""
        data = load_data()
        required_cols = ['location', 'date']
        for col in required_cols:
            assert col in data.columns, f"Missing column: {col}"
    
    def test_load_data_date_column_is_datetime(self):
        """Test that date column is datetime type."""
        data = load_data()
        assert pd.api.types.is_datetime64_any_dtype(data['date'])
    
    @patch('epi_analytics.data._download_owid')
    def test_load_data_uses_cache(self, mock_download):
        """Test that load_data uses cache when available."""
        # Mock successful cache load
        mock_data = pd.DataFrame({
            'location': ['France'],
            'date': [pd.Timestamp('2020-01-01')],
            'total_cases': [100]
        })
        
        with patch('epi_analytics.data._load_from_cache', return_value=mock_data):
            data = load_data(use_cache=True)
            
            # Should not call download if cache works
            mock_download.assert_not_called()
            assert len(data) > 0


class TestCleanData:
    """Test data cleaning function."""
    
    def test_clean_data_removes_duplicates(self):
        """Test that duplicates are removed."""
        dirty_data = pd.DataFrame({
            'location': ['France', 'France', 'Germany'],
            'date': ['2020-01-01', '2020-01-01', '2020-01-01'],
            'total_cases': [100, 100, 200]
        })
        
        clean = _clean_data(dirty_data)
        assert len(clean) == 2  # One duplicate removed
    
    def test_clean_data_converts_date(self):
        """Test that date column is converted to datetime."""
        data = pd.DataFrame({
            'location': ['France'],
            'date': ['2020-01-01'],
            'total_cases': [100]
        })
        
        clean = _clean_data(data)
        assert pd.api.types.is_datetime64_any_dtype(clean['date'])
    
    def test_clean_data_sorts_by_location_and_date(self):
        """Test that data is sorted correctly."""
        data = pd.DataFrame({
            'location': ['Germany', 'France', 'France'],
            'date': ['2020-01-02', '2020-01-02', '2020-01-01'],
            'total_cases': [200, 150, 100]
        })
        
        clean = _clean_data(data)
        
        # Should be sorted by location then date
        assert clean.iloc[0]['location'] == 'France'
        assert clean.iloc[0]['date'] < clean.iloc[1]['date']


class TestLoadSample:
    """Test sample data loading."""
    
    def test_load_sample_returns_dataframe(self):
        """Test that sample data loads successfully."""
        # Note: This will fail if sample data doesn't exist yet
        # In real implementation, we'd create the sample data first
        try:
            data = _load_sample()
            assert isinstance(data, pd.DataFrame)
            assert len(data) > 0
        except FileNotFoundError:
            pytest.skip("Sample data not yet created")
    
    def test_load_sample_has_expected_structure(self):
        """Test that sample data has expected columns."""
        try:
            data = _load_sample()
            expected_cols = ['location', 'date', 'total_cases']
            for col in expected_cols:
                assert col in data.columns
        except FileNotFoundError:
            pytest.skip("Sample data not yet created")


class TestCacheOperations:
    """Test cache loading and saving."""
    
    def test_load_from_cache_returns_none_if_not_exists(self):
        """Test that cache returns None if file doesn't exist."""
        with patch('pathlib.Path.exists', return_value=False):
            result = _load_from_cache()
            assert result is None
    
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.stat')
    @patch('pandas.read_csv')
    def test_load_from_cache_returns_data_if_fresh(self, mock_read_csv, mock_stat, mock_exists):
        """Test that fresh cache data is loaded."""
        import time
        
        # Mock fresh cache (< 24h old)
        mock_stat_result = MagicMock()
        mock_stat_result.st_mtime = time.time() - 3600  # 1 hour ago
        mock_stat.return_value = mock_stat_result
        
        mock_data = pd.DataFrame({'location': ['France'], 'date': ['2020-01-01']})
        mock_read_csv.return_value = mock_data
        
        result = _load_from_cache()
        assert result is not None
        assert isinstance(result, pd.DataFrame)


# Integration test
class TestIntegration:
    """Integration tests for the data module."""
    
    def test_full_load_workflow(self):
        """Test complete data loading workflow."""
        # This should work even without internet (falls back to sample)
        data = load_data()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'location' in data.columns
        assert 'date' in data.columns
        
        # Check data quality
        assert data['location'].notna().all()
        assert pd.api.types.is_datetime64_any_dtype(data['date'])
