"""
Data cleaning pipeline.
Handles missing values, duplicates, outliers, and data quality issues.
"""

import pandas as pd
import numpy as np

from covid_analytics.core.config import get_settings
from covid_analytics.core.logging import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """Pipeline for cleaning COVID-19 data"""
    
    def __init__(self, config: dict | None = None):
        """
        Initialize cleaner with configuration.
        
        Args:
            config: Optional configuration dict
        """
        self.settings = get_settings()
        self.config = config or {}
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run complete cleaning pipeline.
        
        Args:
            df: Raw DataFrame
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("cleaning_started", rows=len(df))
        
        df_clean = df.copy()
        
        # Pipeline steps
        df_clean = self._remove_duplicates(df_clean)
        df_clean = self._fix_data_types(df_clean)
        df_clean = self._handle_missing_values(df_clean)
        df_clean = self._validate_values(df_clean)
        df_clean = self._sort_data(df_clean)
        
        logger.info(
            "cleaning_completed",
            rows_before=len(df),
            rows_after=len(df_clean),
            rows_removed=len(df) - len(df_clean)
        )
        
        return df_clean
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_count = len(df)
        df_dedup = df.drop_duplicates()
        duplicates_removed = initial_count - len(df_dedup)
        
        if duplicates_removed > 0:
            logger.info("duplicates_removed", count=duplicates_removed)
        
        return df_dedup
    
    def _fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types"""
        df_typed = df.copy()
        
        # Convert date column
        if "date" in df_typed.columns:
            df_typed["date"] = pd.to_datetime(df_typed["date"], errors="coerce")
        
        # Convert numeric columns
        numeric_keywords = ["cases", "deaths", "vaccinations", "tests", "total", "new", "rate"]
        for col in df_typed.columns:
            if any(keyword in col.lower() for keyword in numeric_keywords):
                if not pd.api.types.is_numeric_dtype(df_typed[col]):
                    df_typed[col] = pd.to_numeric(df_typed[col], errors="coerce")
        
        return df_typed
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with appropriate strategies"""
        df_filled = df.copy()
        
        for column in df_filled.columns:
            missing_count = df_filled[column].isnull().sum()
            
            if missing_count == 0:
                continue
            
            missing_pct = (missing_count / len(df_filled)) * 100
            
            # Drop column if too many missing values
            if missing_pct > self.settings.max_missing_percentage:
                df_filled = df_filled.drop(columns=[column])
                logger.info(
                    "column_dropped",
                    column=column,
                    missing_pct=f"{missing_pct:.1f}%"
                )
                continue
            
            # Handle numeric columns
            if pd.api.types.is_numeric_dtype(df_filled[column]):
                if missing_pct < 5:
                    # Interpolate for time series
                    if "location" in df_filled.columns:
                        df_filled[column] = df_filled.groupby("location")[column].transform(
                            lambda x: x.interpolate(
                                method=self.settings.interpolation_method,
                                limit_direction="both"
                            )
                        )
                    else:
                        df_filled[column] = df_filled[column].interpolate(
                            method=self.settings.interpolation_method
                        )
                else:
                    # Fill with 0 for higher missing rates
                    df_filled[column] = df_filled[column].fillna(0)
            else:
                # Handle categorical columns
                df_filled[column] = df_filled[column].fillna("Unknown")
        
        return df_filled
    
    def _validate_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and correct invalid values"""
        df_valid = df.copy()
        
        # Remove negative values from count columns
        count_columns = [
            col for col in df_valid.columns
            if any(x in col.lower() for x in ["cases", "deaths", "tests", "vaccinations"])
        ]
        
        for col in count_columns:
            if pd.api.types.is_numeric_dtype(df_valid[col]):
                negative_count = (df_valid[col] < 0).sum()
                if negative_count > 0:
                    df_valid.loc[df_valid[col] < 0, col] = 0
                    logger.info(
                        "negative_values_corrected",
                        column=col,
                        count=negative_count
                    )
        
        # Remove rows with invalid dates
        if "date" in df_valid.columns:
            invalid_dates = df_valid["date"].isnull().sum()
            if invalid_dates > 0:
                df_valid = df_valid[df_valid["date"].notna()]
                logger.info("invalid_dates_removed", count=invalid_dates)
        
        return df_valid
    
    def _sort_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort data by location and date"""
        sort_columns = []
        
        if "location" in df.columns:
            sort_columns.append("location")
        if "date" in df.columns:
            sort_columns.append("date")
        
        if sort_columns:
            df_sorted = df.sort_values(by=sort_columns).reset_index(drop=True)
            return df_sorted
        
        return df
