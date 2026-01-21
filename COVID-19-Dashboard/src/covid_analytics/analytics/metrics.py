"""
Metrics calculator for COVID-19 analytics.
Provides validated calculations for key epidemiological metrics.
"""

from typing import Optional, Tuple
import pandas as pd
import numpy as np

from covid_analytics.core.logging import get_logger

logger = get_logger(__name__)


class MetricsCalculator:
    """Calculate COVID-19 metrics with validation"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize calculator with data.
        
        Args:
            data: DataFrame with COVID-19 data
        """
        self.data = data.copy()
        self._validate_data()
    
    def _validate_data(self) -> None:
        """Validate that data has required columns"""
        required = ["date", "location"]
        missing = [col for col in required if col not in self.data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def mortality_rate(
        self,
        country: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None
    ) -> float:
        """
        Calculate mortality rate (deaths / cases * 100).
        
        Args:
            country: Optional country filter
            date_range: Optional (start_date, end_date) tuple
        
        Returns:
            Mortality rate as percentage
        
        Example:
            >>> calc = MetricsCalculator(data)
            >>> rate = calc.mortality_rate(country="France")
            >>> print(f"Mortality: {rate:.2f}%")
        """
        df = self._filter_data(country, date_range)
        
        if "total_deaths" not in df.columns or "total_cases" not in df.columns:
            logger.warning("missing_columns_for_mortality_rate")
            return 0.0
        
        # Get latest values
        if country:
            latest = df.groupby("location").last()
        else:
            latest = df.iloc[-1:]
        
        total_deaths = latest["total_deaths"].sum()
        total_cases = latest["total_cases"].sum()
        
        if total_cases == 0:
            return 0.0
        
        rate = (total_deaths / total_cases) * 100
        
        logger.info(
            "mortality_rate_calculated",
            country=country,
            rate=f"{rate:.2f}%",
            deaths=int(total_deaths),
            cases=int(total_cases)
        )
        
        return float(rate)
    
    def case_fatality_rate(
        self,
        country: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None
    ) -> float:
        """
        Calculate case fatality rate (new deaths / new cases * 100).
        
        Args:
            country: Optional country filter
            date_range: Optional (start_date, end_date) tuple
        
        Returns:
            Case fatality rate as percentage
        """
        df = self._filter_data(country, date_range)
        
        if "new_deaths" not in df.columns or "new_cases" not in df.columns:
            logger.warning("missing_columns_for_cfr")
            return 0.0
        
        total_new_deaths = df["new_deaths"].sum()
        total_new_cases = df["new_cases"].sum()
        
        if total_new_cases == 0:
            return 0.0
        
        cfr = (total_new_deaths / total_new_cases) * 100
        
        logger.info(
            "cfr_calculated",
            country=country,
            cfr=f"{cfr:.2f}%"
        )
        
        return float(cfr)
    
    def growth_rate(
        self,
        metric: str = "total_cases",
        country: Optional[str] = None,
        window: int = 7
    ) -> pd.Series:
        """
        Calculate growth rate over a rolling window.
        
        Args:
            metric: Column to calculate growth for
            country: Optional country filter
            window: Rolling window size in days
        
        Returns:
            Series with growth rates
        """
        df = self._filter_data(country, None)
        
        if metric not in df.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        if country:
            df = df[df["location"] == country].copy()
        
        df = df.sort_values("date")
        growth = df[metric].pct_change(periods=window) * 100
        
        logger.info(
            "growth_rate_calculated",
            metric=metric,
            country=country,
            window=window
        )
        
        return growth
    
    def daily_average(
        self,
        metric: str,
        country: Optional[str] = None,
        window: int = 7
    ) -> pd.Series:
        """
        Calculate rolling average for a metric.
        
        Args:
            metric: Column to average
            country: Optional country filter
            window: Rolling window size
        
        Returns:
            Series with rolling averages
        """
        df = self._filter_data(country, None)
        
        if metric not in df.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        if country:
            df = df[df["location"] == country].copy()
        
        df = df.sort_values("date")
        avg = df[metric].rolling(window=window, min_periods=1).mean()
        
        return avg
    
    def total_by_country(self, metric: str) -> pd.DataFrame:
        """
        Get total values by country.
        
        Args:
            metric: Column to sum
        
        Returns:
            DataFrame with totals by country
        """
        if metric not in self.data.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        if "location" not in self.data.columns:
            raise ValueError("Data must have 'location' column")
        
        totals = self.data.groupby("location")[metric].max().sort_values(ascending=False)
        
        return totals.to_frame()
    
    def compare_countries(
        self,
        countries: list[str],
        metric: str,
        normalize: bool = False
    ) -> pd.DataFrame:
        """
        Compare metric across countries.
        
        Args:
            countries: List of country names
            metric: Metric to compare
            normalize: Normalize by population if True
        
        Returns:
            DataFrame with comparison
        """
        if metric not in self.data.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        df = self.data[self.data["location"].isin(countries)].copy()
        
        if normalize and "population" in df.columns:
            df[f"{metric}_per_million"] = (
                df[metric] / df["population"] * 1_000_000
            )
            metric = f"{metric}_per_million"
        
        comparison = df.pivot_table(
            values=metric,
            index="date",
            columns="location",
            aggfunc="max"
        )
        
        return comparison
    
    def _filter_data(
        self,
        country: Optional[str],
        date_range: Optional[Tuple[str, str]]
    ) -> pd.DataFrame:
        """Filter data by country and date range"""
        df = self.data.copy()
        
        if country:
            df = df[df["location"] == country]
        
        if date_range:
            start, end = date_range
            df["date"] = pd.to_datetime(df["date"])
            df = df[(df["date"] >= start) & (df["date"] <= end)]
        
        return df
