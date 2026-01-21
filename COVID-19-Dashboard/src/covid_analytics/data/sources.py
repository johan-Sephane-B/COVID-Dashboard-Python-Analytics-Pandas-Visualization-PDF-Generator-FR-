"""
Data source abstraction and implementations.
Provides unified interface for loading data from multiple sources.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import hashlib

import pandas as pd
import requests

from covid_analytics.core.config import get_settings
from covid_analytics.core.logging import get_logger
from covid_analytics.core.exceptions import DataLoadError, APIError

logger = get_logger(__name__)


class DataSource:
    """Unified interface for data sources"""
    
    @staticmethod
    def from_owid(
        cache: bool = True,
        refresh_interval: str = "24h",
        fallback_to_synthetic: bool = False
    ) -> pd.DataFrame:
        """
        Load data from Our World in Data API.
        
        Args:
            cache: Enable local caching
            refresh_interval: Cache refresh interval (e.g., "24h", "1d")
            fallback_to_synthetic: Use synthetic data if API fails
        
        Returns:
            DataFrame with COVID-19 data
        
        Raises:
            DataLoadError: If data loading fails
        """
        settings = get_settings()
        
        if cache:
            cached_data = _load_from_cache(settings.cache_dir / "owid_data.csv", refresh_interval)
            if cached_data is not None:
                logger.info("data_loaded_from_cache", rows=len(cached_data))
                return cached_data
        
        # Try primary URL
        try:
            logger.info("fetching_owid_data", url=settings.owid_url)
            df = pd.read_csv(settings.owid_url)
            
            if cache:
                _save_to_cache(df, settings.cache_dir / "owid_data.csv")
            
            logger.info("data_loaded_from_api", rows=len(df), columns=len(df.columns))
            return df
            
        except Exception as e:
            logger.warning("primary_url_failed", error=str(e))
            
            # Try backup URL
            try:
                logger.info("trying_backup_url", url=settings.owid_backup_url)
                df = pd.read_csv(settings.owid_backup_url)
                
                if cache:
                    _save_to_cache(df, settings.cache_dir / "owid_data.csv")
                
                logger.info("data_loaded_from_backup", rows=len(df))
                return df
                
            except Exception as backup_error:
                logger.error("backup_url_failed", error=str(backup_error))
                
                if fallback_to_synthetic:
                    logger.warning("falling_back_to_synthetic")
                    return DataSource.synthetic()
                
                raise DataLoadError(
                    f"Failed to load from both primary and backup URLs: {e}, {backup_error}"
                )
    
    @staticmethod
    def from_csv(filepath: str | Path) -> pd.DataFrame:
        """
        Load data from local CSV file.
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            DataFrame with COVID-19 data
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise DataLoadError(f"File not found: {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            logger.info("data_loaded_from_file", path=str(filepath), rows=len(df))
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load CSV: {e}")
    
    @staticmethod
    def synthetic(countries: int = 10, days: int = 365, seed: int = 42) -> pd.DataFrame:
        """
        Generate synthetic COVID-19 data for testing.
        
        Args:
            countries: Number of countries to generate
            days: Number of days of data
            seed: Random seed for reproducibility
        
        Returns:
            DataFrame with synthetic data
        """
        import numpy as np
        
        np.random.seed(seed)
        
        country_names = [
            "France", "Germany", "Italy", "Spain", "United Kingdom",
            "United States", "Canada", "Australia", "Japan", "Brazil"
        ][:countries]
        
        data = []
        start_date = datetime(2020, 1, 1)
        
        for country in country_names:
            base_cases = np.random.randint(100, 1000)
            growth_rate = np.random.uniform(1.01, 1.05)
            
            for day in range(days):
                date = start_date + timedelta(days=day)
                total_cases = int(base_cases * (growth_rate ** day))
                total_deaths = int(total_cases * np.random.uniform(0.01, 0.03))
                new_cases = int(total_cases * np.random.uniform(0.01, 0.05))
                new_deaths = int(new_cases * np.random.uniform(0.01, 0.03))
                
                data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "location": country,
                    "total_cases": total_cases,
                    "total_deaths": total_deaths,
                    "new_cases": new_cases,
                    "new_deaths": new_deaths,
                })
        
        df = pd.DataFrame(data)
        logger.info("synthetic_data_generated", countries=countries, days=days, rows=len(df))
        return df


def _load_from_cache(cache_path: Path, refresh_interval: str) -> Optional[pd.DataFrame]:
    """Load data from cache if valid"""
    if not cache_path.exists():
        return None
    
    # Parse refresh interval
    hours = _parse_interval(refresh_interval)
    
    # Check if cache is still valid
    cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
    if cache_age > timedelta(hours=hours):
        logger.info("cache_expired", age_hours=cache_age.total_seconds() / 3600)
        return None
    
    try:
        df = pd.read_csv(cache_path)
        return df
    except Exception as e:
        logger.warning("cache_load_failed", error=str(e))
        return None


def _save_to_cache(df: pd.DataFrame, cache_path: Path) -> None:
    """Save data to cache"""
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache_path, index=False)
        logger.info("data_cached", path=str(cache_path))
    except Exception as e:
        logger.warning("cache_save_failed", error=str(e))


def _parse_interval(interval: str) -> int:
    """Parse interval string to hours"""
    if interval.endswith("h"):
        return int(interval[:-1])
    elif interval.endswith("d"):
        return int(interval[:-1]) * 24
    else:
        return 24  # Default to 24 hours
