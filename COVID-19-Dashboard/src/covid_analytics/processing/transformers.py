"""
Data transformers for business logic transformations.
"""

import pandas as pd
import numpy as np

from covid_analytics.core.logging import get_logger

logger = get_logger(__name__)


class DataTransformer:
    """Business logic transformations"""
    
    @staticmethod
    def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived metrics like mortality rate, growth rate, etc.
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with additional derived columns
        """
        df_transformed = df.copy()
        
        # Mortality rate
        if "total_deaths" in df_transformed.columns and "total_cases" in df_transformed.columns:
            df_transformed["mortality_rate"] = (
                df_transformed["total_deaths"] / df_transformed["total_cases"] * 100
            ).replace([np.inf, -np.inf], np.nan)
        
        # Case fatality rate (CFR)
        if "new_deaths" in df_transformed.columns and "new_cases" in df_transformed.columns:
            df_transformed["case_fatality_rate"] = (
                df_transformed["new_deaths"] / df_transformed["new_cases"] * 100
            ).replace([np.inf, -np.inf], np.nan)
        
        # Growth rate (7-day)
        if "location" in df_transformed.columns and "total_cases" in df_transformed.columns:
            df_transformed["growth_rate_7d"] = df_transformed.groupby("location")["total_cases"].pct_change(periods=7) * 100
        
        logger.info("derived_metrics_added")
        return df_transformed
    
    @staticmethod
    def normalize_by_population(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize metrics by population.
        
        Args:
            df: Input DataFrame with population column
        
        Returns:
            DataFrame with normalized columns
        """
        if "population" not in df.columns:
            logger.warning("population_column_missing")
            return df
        
        df_normalized = df.copy()
        
        metrics_to_normalize = [
            "total_cases", "new_cases", "total_deaths", "new_deaths",
            "total_vaccinations", "new_vaccinations"
        ]
        
        for metric in metrics_to_normalize:
            if metric in df_normalized.columns:
                normalized_col = f"{metric}_per_million"
                df_normalized[normalized_col] = (
                    df_normalized[metric] / df_normalized["population"] * 1_000_000
                ).replace([np.inf, -np.inf], np.nan)
        
        logger.info("metrics_normalized_by_population")
        return df_normalized
    
    @staticmethod
    def aggregate_by_period(
        df: pd.DataFrame,
        period: str = "W",
        agg_func: str = "sum"
    ) -> pd.DataFrame:
        """
        Aggregate data by time period.
        
        Args:
            df: Input DataFrame with date column
            period: Pandas period string ('D', 'W', 'M', 'Y')
            agg_func: Aggregation function ('sum', 'mean', 'max', etc.)
        
        Returns:
            Aggregated DataFrame
        """
        if "date" not in df.columns:
            raise ValueError("DataFrame must have 'date' column")
        
        df_agg = df.copy()
        df_agg["date"] = pd.to_datetime(df_agg["date"])
        
        # Group by location and period
        if "location" in df_agg.columns:
            df_agg = df_agg.set_index("date").groupby(
                ["location", pd.Grouper(freq=period)]
            ).agg(agg_func).reset_index()
        else:
            df_agg = df_agg.set_index("date").resample(period).agg(agg_func).reset_index()
        
        logger.info("data_aggregated", period=period, agg_func=agg_func)
        return df_agg
