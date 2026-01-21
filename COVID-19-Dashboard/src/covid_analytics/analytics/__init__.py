"""Analytics layer - business logic and calculations"""

from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector

__all__ = [
    "MetricsCalculator",
    "TrendDetector",
]
