"""
Trend detection for COVID-19 data.
Identifies upward/downward trends and anomalies.
"""

from typing import Optional, Literal
from enum import Enum
import pandas as pd
import numpy as np

from covid_analytics.core.logging import get_logger

logger = get_logger(__name__)


class TrendDirection(str, Enum):
    """Trend direction enumeration"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    UNKNOWN = "unknown"


class TrendDetector:
    """Detect trends in COVID-19 time series data"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize trend detector.
        
        Args:
            data: DataFrame with COVID-19 data
        """
        self.data = data.copy()
        self._validate_data()
    
    def _validate_data(self) -> None:
        """Validate data has required columns"""
        if "date" not in self.data.columns:
            raise ValueError("Data must have 'date' column")
        
        self.data["date"] = pd.to_datetime(self.data["date"])
    
    def detect(
        self,
        metric: str,
        country: Optional[str] = None,
        window: int = 7,
        threshold: float = 0.1
    ) -> pd.DataFrame:
        """
        Detect trends in a metric.
        
        Args:
            metric: Column to analyze
            country: Optional country filter
            window: Window size for trend calculation
            threshold: Threshold for trend detection (10% = 0.1)
        
        Returns:
            DataFrame with trend information
        """
        if metric not in self.data.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        df = self.data.copy()
        
        if country:
            df = df[df["location"] == country]
        
        df = df.sort_values("date")
        
        # Calculate rolling average
        df["rolling_avg"] = df[metric].rolling(window=window, min_periods=1).mean()
        
        # Calculate percentage change
        df["pct_change"] = df["rolling_avg"].pct_change(periods=window)
        
        # Determine trend direction
        df["trend"] = df["pct_change"].apply(
            lambda x: self._classify_trend(x, threshold)
        )
        
        logger.info(
            "trends_detected",
            metric=metric,
            country=country,
            window=window,
            threshold=threshold
        )
        
        return df[["date", "location", metric, "rolling_avg", "pct_change", "trend"]]
    
    def _classify_trend(self, pct_change: float, threshold: float) -> str:
        """Classify trend based on percentage change"""
        if pd.isna(pct_change):
            return TrendDirection.UNKNOWN
        
        if pct_change > threshold:
            return TrendDirection.INCREASING
        elif pct_change < -threshold:
            return TrendDirection.DECREASING
        else:
            return TrendDirection.STABLE
    
    def detect_peaks(
        self,
        metric: str,
        country: Optional[str] = None,
        prominence: float = 0.2
    ) -> pd.DataFrame:
        """
        Detect peaks (local maxima) in time series.
        
        Args:
            metric: Column to analyze
            country: Optional country filter
            prominence: Minimum prominence for peak detection
        
        Returns:
            DataFrame with peak dates and values
        """
        from scipy.signal import find_peaks
        
        df = self.data.copy()
        
        if country:
            df = df[df["location"] == country]
        
        df = df.sort_values("date")
        
        if metric not in df.columns:
            raise ValueError(f"Metric '{metric}' not found")
        
        values = df[metric].values
        peaks, properties = find_peaks(values, prominence=prominence * values.max())
        
        peak_data = df.iloc[peaks].copy()
        peak_data["peak_value"] = values[peaks]
        
        logger.info(
            "peaks_detected",
            metric=metric,
            country=country,
            num_peaks=len(peaks)
        )
        
        return peak_data[["date", "location", metric, "peak_value"]]
    
    def detect_anomalies(
        self,
        metric: str,
        country: Optional[str] = None,
        std_threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Detect anomalies using standard deviation method.
        
        Args:
            metric: Column to analyze
            country: Optional country filter
            std_threshold: Number of standard deviations for anomaly
        
        Returns:
            DataFrame with anomalies
        """
        df = self.data.copy()
        
        if country:
            df = df[df["location"] == country]
        
        if metric not in df.columns:
            raise ValueError(f"Metric '{metric}' not found")
        
        df = df.sort_values("date")
        
        # Calculate statistics
        mean = df[metric].mean()
        std = df[metric].std()
        
        # Detect anomalies
        df["z_score"] = (df[metric] - mean) / std
        df["is_anomaly"] = df["z_score"].abs() > std_threshold
        
        anomalies = df[df["is_anomaly"]].copy()
        
        logger.info(
            "anomalies_detected",
            metric=metric,
            country=country,
            num_anomalies=len(anomalies),
            threshold=std_threshold
        )
        
        return anomalies[["date", "location", metric, "z_score"]]
    
    def get_trend_summary(
        self,
        metric: str,
        country: Optional[str] = None,
        window: int = 7
    ) -> dict:
        """
        Get summary of current trend.
        
        Args:
            metric: Column to analyze
            country: Optional country filter
            window: Window for trend calculation
        
        Returns:
            Dictionary with trend summary
        """
        trends = self.detect(metric, country, window)
        
        if len(trends) == 0:
            return {"trend": TrendDirection.UNKNOWN, "change": 0.0}
        
        latest = trends.iloc[-1]
        
        summary = {
            "trend": latest["trend"],
            "change": float(latest["pct_change"]) if not pd.isna(latest["pct_change"]) else 0.0,
            "current_value": float(latest[metric]),
            "rolling_avg": float(latest["rolling_avg"]),
            "date": latest["date"].strftime("%Y-%m-%d")
        }
        
        return summary
