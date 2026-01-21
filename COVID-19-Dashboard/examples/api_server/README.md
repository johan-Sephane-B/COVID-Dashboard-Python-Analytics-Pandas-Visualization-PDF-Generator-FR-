# COVID Analytics - REST API

FastAPI-based REST API for COVID-19 data and analytics.

## Features

- 🚀 Fast and async API with FastAPI
- 📊 Real-time COVID-19 data endpoints
- 📈 Analytics endpoints (metrics, trends)
- 📝 Automatic OpenAPI documentation
- 🔒 CORS enabled for web applications

## Installation

```bash
# Install the library with API support
pip install -e ".[api]"
```

## Usage

### Start the API server

```bash
# Development mode
uvicorn examples.api_server.main:app --reload

# Production mode
uvicorn examples.api_server.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Get Countries

```bash
GET /countries
```

Response:
```json
{
  "countries": ["France", "Germany", "Italy", ...],
  "count": 200
}
```

### Get Country Data

```bash
GET /data/{country}?start_date=2020-01-01&end_date=2023-12-31&limit=100
```

Parameters:
- `country` (path): Country name
- `start_date` (query, optional): Start date (YYYY-MM-DD)
- `end_date` (query, optional): End date (YYYY-MM-DD)
- `limit` (query, optional): Max results (default: 100, max: 1000)

Response:
```json
[
  {
    "date": "2020-01-01",
    "location": "France",
    "total_cases": 1000.0,
    "total_deaths": 10.0,
    "new_cases": 100.0,
    "new_deaths": 1.0
  },
  ...
]
```

### Get Country Metrics

```bash
GET /metrics/{country}?start_date=2020-01-01&end_date=2023-12-31
```

Parameters:
- `country` (path): Country name
- `start_date` (query, optional): Start date
- `end_date` (query, optional): End date

Response:
```json
{
  "country": "France",
  "mortality_rate": 2.34,
  "case_fatality_rate": 1.89,
  "total_cases": 1000000.0,
  "total_deaths": 23400.0
}
```

### Get Country Trends

```bash
GET /trends/{country}?metric=total_cases&window=7
```

Parameters:
- `country` (path): Country name
- `metric` (query): Metric to analyze (total_cases, total_deaths, new_cases, new_deaths)
- `window` (query): Rolling window in days (1-30)

Response:
```json
{
  "country": "France",
  "trend": "increasing",
  "change": 5.2,
  "current_value": 1000000.0,
  "rolling_avg": 950000.0,
  "date": "2023-12-31"
}
```

### Refresh Data

```bash
POST /refresh
```

Response:
```json
{
  "status": "success",
  "message": "Data refreshed"
}
```

## Example Usage

### Python

```python
import requests

# Get countries
response = requests.get("http://localhost:8000/countries")
countries = response.json()["countries"]

# Get data for France
response = requests.get("http://localhost:8000/data/France?limit=10")
data = response.json()

# Get metrics
response = requests.get("http://localhost:8000/metrics/France")
metrics = response.json()
print(f"Mortality rate: {metrics['mortality_rate']:.2f}%")

# Get trends
response = requests.get("http://localhost:8000/trends/France?metric=total_cases&window=7")
trends = response.json()
print(f"Trend: {trends['trend']} ({trends['change']:.1f}% change)")
```

### JavaScript

```javascript
// Get countries
fetch('http://localhost:8000/countries')
  .then(response => response.json())
  .then(data => console.log(data.countries));

// Get metrics
fetch('http://localhost:8000/metrics/France')
  .then(response => response.json())
  .then(data => console.log(`Mortality: ${data.mortality_rate}%`));
```

### cURL

```bash
# Get countries
curl http://localhost:8000/countries

# Get data
curl "http://localhost:8000/data/France?limit=10"

# Get metrics
curl http://localhost:8000/metrics/France

# Get trends
curl "http://localhost:8000/trends/France?metric=total_cases&window=7"
```

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Success
- `404 Not Found`: Country not found
- `422 Unprocessable Entity`: Invalid parameters
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "detail": "Country 'InvalidCountry' not found"
}
```

## Performance

- Data is cached in memory for fast responses
- Use `/refresh` endpoint to update cached data
- Supports up to 1000 results per request

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -e ".[api]"

CMD ["uvicorn", "examples.api_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Configure via `.env` file (see `.env.example`).
