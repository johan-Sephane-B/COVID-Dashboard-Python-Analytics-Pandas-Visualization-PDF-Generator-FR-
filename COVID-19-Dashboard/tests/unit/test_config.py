"""Tests for configuration module"""

import pytest
from pathlib import Path

from covid_analytics.core.config import Settings, get_settings


class TestSettings:
    """Test Settings class"""
    
    def test_default_settings(self):
        """Test default configuration values"""
        settings = Settings()
        
        assert settings.app_name == "COVID Analytics"
        assert settings.app_version == "1.0.0"
        assert settings.debug is False
        assert settings.cache_enabled is True
        assert settings.cache_ttl_hours == 24
        assert settings.log_level == "INFO"
    
    def test_custom_settings(self):
        """Test custom configuration"""
        settings = Settings(
            debug=True,
            log_level="DEBUG",
            cache_ttl_hours=48
        )
        
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.cache_ttl_hours == 48
    
    def test_ensure_directories(self, tmp_path, monkeypatch):
        """Test directory creation"""
        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        
        settings = Settings()
        settings.ensure_directories()
        
        assert settings.data_dir.exists()
        assert settings.cache_dir.exists()
        assert settings.output_dir.exists()
    
    def test_get_settings_cached(self):
        """Test that get_settings returns cached instance"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2  # Same instance
