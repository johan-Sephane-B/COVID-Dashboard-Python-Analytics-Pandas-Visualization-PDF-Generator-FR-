"""
Pydantic schemas for data validation.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class CovidDataSchema(BaseModel):
    """Schema for COVID-19 data records"""
    
    date: date = Field(description="Date of the record")
    location: str = Field(description="Country or region name")
    
    # Cases
    total_cases: Optional[float] = Field(default=None, ge=0)
    new_cases: Optional[float] = Field(default=None)
    total_cases_per_million: Optional[float] = Field(default=None, ge=0)
    new_cases_per_million: Optional[float] = Field(default=None)
    
    # Deaths
    total_deaths: Optional[float] = Field(default=None, ge=0)
    new_deaths: Optional[float] = Field(default=None)
    total_deaths_per_million: Optional[float] = Field(default=None, ge=0)
    new_deaths_per_million: Optional[float] = Field(default=None)
    
    # Vaccinations
    people_vaccinated: Optional[float] = Field(default=None, ge=0)
    people_fully_vaccinated: Optional[float] = Field(default=None, ge=0)
    total_vaccinations: Optional[float] = Field(default=None, ge=0)
    new_vaccinations: Optional[float] = Field(default=None, ge=0)
    
    # Testing
    total_tests: Optional[float] = Field(default=None, ge=0)
    new_tests: Optional[float] = Field(default=None, ge=0)
    
    # Population
    population: Optional[float] = Field(default=None, ge=0)
    
    @field_validator("location")
    @classmethod
    def location_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Location cannot be empty")
        return v.strip()
    
    class Config:
        str_strip_whitespace = True
        validate_assignment = True


class DataQualityReport(BaseModel):
    """Report on data quality"""
    
    total_rows: int
    total_columns: int
    missing_values: dict[str, int]
    duplicate_rows: int
    date_range: tuple[date, date]
    countries: int
    
    class Config:
        frozen = True
