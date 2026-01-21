"""
Configuration management using Pydantic Settings.
Supports environment variables and .env files.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    app_name: str = "COVID Analytics"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Paths
    data_dir: Path = Field(default=Path("data"), description="Data directory")
    raw_data_dir: Path = Field(default=Path("data/raw"), description="Raw data directory")
    processed_data_dir: Path = Field(
        default=Path("data/processed"),
        description="Processed data directory"
    )
    cache_dir: Path = Field(default=Path("data/cache"), description="Cache directory")
    output_dir: Path = Field(default=Path("output"), description="Output directory")
    
    # Data Sources
    owid_url: str = Field(
        default="https://covid.ourworldindata.org/data/owid-covid-data.csv",
        description="Our World in Data CSV URL"
    )
    owid_backup_url: str = Field(
        default="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
        description="Backup URL for OWID data"
    )
    
    # Cache settings
    cache_enabled: bool = Field(default=True, description="Enable data caching")
    cache_ttl_hours: int = Field(default=24, description="Cache TTL in hours")
    
    # Processing
    max_missing_percentage: float = Field(
        default=50.0,
        description="Max percentage of missing values before dropping column"
    )
    interpolation_method: str = Field(
        default="linear",
        description="Method for interpolating missing values"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json or text)")
    log_file: Optional[Path] = Field(default=None, description="Log file path")
    
    # Performance
    chunk_size: int = Field(default=10000, description="Chunk size for large datasets")
    n_jobs: int = Field(default=-1, description="Number of parallel jobs (-1 = all CPUs)")
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        for dir_path in [
            self.data_dir,
            self.raw_data_dir,
            self.processed_data_dir,
            self.cache_dir,
            self.output_dir,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.ensure_directories()
    return settings
