"""
Data loader with validation and type conversion.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from covid_analytics.core.logging import get_logger
from covid_analytics.core.exceptions import DataLoadError

logger = get_logger(__name__)


class DataLoader:
    """Handles data loading with validation"""
    
    @staticmethod
    def load(
        filepath: str | Path,
        parse_dates: bool = True,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Load and validate COVID-19 data.
        
        Args:
            filepath: Path to data file
            parse_dates: Automatically parse date columns
            validate: Validate data schema
        
        Returns:
            Loaded and validated DataFrame
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise DataLoadError(f"File not found: {filepath}")
        
        try:
            # Load CSV
            df = pd.read_csv(
                filepath,
                low_memory=False
            )
            
            # Parse dates
            if parse_dates and "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
            
            logger.info(
                "data_loaded",
                path=str(filepath),
                rows=len(df),
                columns=len(df.columns)
            )
            
            # Validate if requested
            if validate:
                _validate_schema(df)
            
            return df
            
        except Exception as e:
            raise DataLoadError(f"Failed to load data: {e}")
    
    @staticmethod
    def get_info(df: pd.DataFrame) -> dict:
        """Get summary information about the dataset"""
        info = {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": df.memory_usage(deep=True).sum() / 1024**2,
            "dtypes": df.dtypes.value_counts().to_dict(),
        }
        
        if "date" in df.columns:
            info["date_range"] = {
                "min": df["date"].min(),
                "max": df["date"].max(),
            }
        
        if "location" in df.columns:
            info["countries"] = df["location"].nunique()
        
        # Missing values
        missing = df.isnull().sum()
        info["missing_values"] = missing[missing > 0].to_dict()
        
        return info


def _validate_schema(df: pd.DataFrame) -> None:
    """Validate that DataFrame has required columns"""
    required_columns = ["date", "location"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise DataLoadError(f"Missing required columns: {missing_columns}")
    
    logger.info("schema_validated", columns=list(df.columns))
