"""
COVID Analytics - Professional Python Library for Pandemic Data Analysis

A comprehensive library for loading, cleaning, analyzing, and visualizing pandemic data.
Designed for researchers, data scientists, and analysts.

Example:
    >>> from covid_analytics import DataSource, Analytics
    >>> data = DataSource.from_owid(cache=True)
    >>> analytics = Analytics(data)
    >>> mortality = analytics.calculate_mortality_rate(country="France")
"""

__version__ = "1.0.0"
__author__ = "COVID Analytics Team"
__license__ = "MIT"

# Core imports
from covid_analytics.core.config import get_settings
from covid_analytics.core.logging import get_logger

# Data layer
from covid_analytics.data.sources import DataSource
from covid_analytics.data.loaders import DataLoader

# Processing layer
from covid_analytics.processing.cleaners import DataCleaner
from covid_analytics.processing.transformers import DataTransformer

# Analytics layer
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector

# Convenience classes
class Analytics:
    """High-level analytics interface"""
    def __init__(self, data):
        self.data = data
        self.metrics = MetricsCalculator(data)
        self.trends = TrendDetector(data)
    
    def calculate_mortality_rate(self, country=None, date_range=None):
        """Calculate mortality rate"""
        return self.metrics.mortality_rate(country=country, date_range=date_range)

__all__ = [
    "__version__",
    "get_settings",
    "get_logger",
    "DataSource",
    "DataLoader",
    "DataCleaner",
    "DataTransformer",
    "MetricsCalculator",
    "TrendDetector",
    "Analytics",
]
