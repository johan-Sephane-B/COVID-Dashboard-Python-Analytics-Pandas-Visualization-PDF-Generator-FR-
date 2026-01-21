"""
COVID Analytics - FastAPI REST API
Provides REST endpoints for COVID-19 data and analytics
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
import pandas as pd

from covid_analytics.data.sources import DataSource
from covid_analytics.processing.cleaners import DataCleaner
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector

# Initialize FastAPI app
app = FastAPI(
    title="COVID Analytics API",
    description="REST API for COVID-19 data analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class HealthResponse(BaseModel):
    status: str
    version: str

class CountryData(BaseModel):
    date: str
    location: str
    total_cases: Optional[float]
    total_deaths: Optional[float]
    new_cases: Optional[float]
    new_deaths: Optional[float]

class MetricsResponse(BaseModel):
    country: str
    mortality_rate: float
    case_fatality_rate: float
    total_cases: float
    total_deaths: float

class TrendResponse(BaseModel):
    country: str
    trend: str
    change: float
    current_value: float
    rolling_avg: float
    date: str

class CountryList(BaseModel):
    countries: List[str]
    count: int

# Cache for data
_data_cache = None

def get_data(refresh: bool = False) -> pd.DataFrame:
    """Get cached or fresh data"""
    global _data_cache
    
    if _data_cache is None or refresh:
        data = DataSource.from_owid(cache=True)
        cleaner = DataCleaner()
        _data_cache = cleaner.clean(data)
    
    return _data_cache


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/countries", response_model=CountryList)
async def get_countries():
    """Get list of available countries"""
    data = get_data()
    countries = sorted(data['location'].unique().tolist())
    
    return {
        "countries": countries,
        "count": len(countries)
    }


@app.get("/data/{country}", response_model=List[CountryData])
async def get_country_data(
    country: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(default=100, le=1000)
):
    """Get COVID-19 data for a specific country"""
    data = get_data()
    
    # Filter by country
    country_data = data[data['location'] == country].copy()
    
    if len(country_data) == 0:
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found")
    
    # Filter by date range
    if start_date:
        country_data = country_data[pd.to_datetime(country_data['date']) >= pd.to_datetime(start_date)]
    
    if end_date:
        country_data = country_data[pd.to_datetime(country_data['date']) <= pd.to_datetime(end_date)]
    
    # Limit results
    country_data = country_data.tail(limit)
    
    # Convert to response format
    result = []
    for _, row in country_data.iterrows():
        result.append({
            "date": str(row['date']),
            "location": row['location'],
            "total_cases": float(row['total_cases']) if pd.notna(row.get('total_cases')) else None,
            "total_deaths": float(row['total_deaths']) if pd.notna(row.get('total_deaths')) else None,
            "new_cases": float(row['new_cases']) if pd.notna(row.get('new_cases')) else None,
            "new_deaths": float(row['new_deaths']) if pd.notna(row.get('new_deaths')) else None,
        })
    
    return result


@app.get("/metrics/{country}", response_model=MetricsResponse)
async def get_country_metrics(
    country: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Get analytics metrics for a specific country"""
    data = get_data()
    
    # Check if country exists
    if country not in data['location'].values:
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found")
    
    # Filter by date range if provided
    filtered_data = data.copy()
    if start_date or end_date:
        filtered_data = data[data['location'] == country].copy()
        if start_date:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']) >= pd.to_datetime(start_date)]
        if end_date:
            filtered_data = filtered_data[pd.to_datetime(filtered_data['date']) <= pd.to_datetime(end_date)]
    
    # Calculate metrics
    metrics_calc = MetricsCalculator(filtered_data)
    
    mortality = metrics_calc.mortality_rate(country=country)
    cfr = metrics_calc.case_fatality_rate(country=country)
    
    # Get latest values
    country_data = filtered_data[filtered_data['location'] == country]
    if len(country_data) == 0:
        raise HTTPException(status_code=404, detail=f"No data found for '{country}' in specified date range")
    
    latest = country_data.iloc[-1]
    
    return {
        "country": country,
        "mortality_rate": mortality,
        "case_fatality_rate": cfr,
        "total_cases": float(latest.get('total_cases', 0)) if pd.notna(latest.get('total_cases')) else 0.0,
        "total_deaths": float(latest.get('total_deaths', 0)) if pd.notna(latest.get('total_deaths')) else 0.0
    }


@app.get("/trends/{country}", response_model=TrendResponse)
async def get_country_trends(
    country: str,
    metric: str = Query(default="total_cases", regex="^(total_cases|total_deaths|new_cases|new_deaths)$"),
    window: int = Query(default=7, ge=1, le=30)
):
    """Get trend analysis for a specific country"""
    data = get_data()
    
    # Check if country exists
    if country not in data['location'].values:
        raise HTTPException(status_code=404, detail=f"Country '{country}' not found")
    
    # Detect trends
    detector = TrendDetector(data)
    
    try:
        summary = detector.get_trend_summary(
            metric=metric,
            country=country,
            window=window
        )
        
        return {
            "country": country,
            "trend": summary['trend'],
            "change": summary['change'],
            "current_value": summary['current_value'],
            "rolling_avg": summary['rolling_avg'],
            "date": summary['date']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating trends: {str(e)}")


@app.post("/refresh")
async def refresh_data():
    """Refresh cached data"""
    global _data_cache
    _data_cache = None
    get_data(refresh=True)
    
    return {"status": "success", "message": "Data refreshed"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
