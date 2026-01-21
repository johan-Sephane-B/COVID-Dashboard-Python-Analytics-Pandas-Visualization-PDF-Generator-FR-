# Migration Guide - COVID Dashboard → Epi Analytics

## Overview

This guide helps you migrate from the old COVID-19 Dashboard to the new **Epi Analytics v0.5.0-beta** library.

## Key Changes

### 1. Project Identity

**Before**: Confused mix of dashboard + library + PDF generator  
**After**: Pure Python library with separate examples

### 2. Installation

**Before**:
```bash
git clone <repo>
cd COVID-19-Dashboard
pip install -r requirements.txt
# Then figure out which files to run...
```

**After**:
```bash
pip install epi-analytics
# Done! Ready to use
```

### 3. API Changes

#### Loading Data

**Before**:
```python
from scripts.data_loader import load_covid_data
from scripts.data_cleaner import clean_covid_data

df = load_covid_data("data/raw/covid_data.csv")
df = clean_covid_data(df)
```

**After**:
```python
from epi_analytics import load_data

data = load_data()  # Auto-downloads, auto-cleans, auto-caches
```

#### Calculating Metrics

**Before**:
```python
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.core.config import Settings

settings = Settings()
calc = MetricsCalculator(data, settings)
mortality = calc.calculate_mortality_rate(country="France")
```

**After**:
```python
from epi_analytics import analyze

mortality = analyze(data, metric="mortality", country="France")
```

#### Visualizations

**Before**:
```python
from covid_analytics.visualization.charts import ChartGenerator
from covid_analytics.core.config import Settings

settings = Settings()
gen = ChartGenerator(data, settings)
fig = gen.create_timeline(countries=["France", "Germany"])
```

**After**:
```python
from epi_analytics import visualize

fig = visualize(data, chart_type="timeline", countries=["France", "Germany"])
fig.show()
```

## Migration Steps

### Step 1: Identify Your Use Case

**If you were using the Streamlit dashboard**:
- The dashboard is now a separate example
- See `examples_new/` for new dashboard code
- Or deploy your own using the library

**If you were using the library**:
- Follow the API migration below
- Most functionality is preserved, just simpler

**If you were generating PDFs**:
- PDF generation is not in v0.5.0-beta
- You can build it yourself using the library
- Or wait for future versions

### Step 2: Update Imports

Replace all old imports:

```python
# OLD - Don't use these anymore
from scripts.data_loader import *
from scripts.data_cleaner import *
from scripts.data_utils import *
from covid_analytics.data.sources import DataSource
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.visualization.charts import ChartGenerator

# NEW - Use these instead
from epi_analytics import load_data, analyze, visualize
```

### Step 3: Update Data Loading

**Old code**:
```python
# Option 1: From local file
df = load_covid_data("data/raw/covid_data.csv")
df = clean_covid_data(df)

# Option 2: From DataSource
from covid_analytics.data.sources import DataSource
ds = DataSource()
df = ds.from_owid(cache=True)
```

**New code**:
```python
# One line, works everywhere
data = load_data()

# Force re-download if needed
data = load_data(force_download=True)
```

### Step 4: Update Analysis Code

**Old code**:
```python
from covid_analytics.analytics.metrics import MetricsCalculator

calc = MetricsCalculator(data)

# Mortality
mortality = calc.calculate_mortality_rate(country="France")

# Growth rate
growth = calc.calculate_growth_rate(country="France", window=7)

# Peaks
peaks = calc.detect_peaks(country="France", metric="new_cases")
```

**New code**:
```python
from epi_analytics import analyze

# Mortality
mortality = analyze(data, metric="mortality", country="France")

# Growth rate
growth = analyze(data, metric="growth", country="France")

# Peaks
peaks = analyze(data, metric="peaks", country="France", metric_col="new_cases")
```

### Step 5: Update Visualization Code

**Old code**:
```python
from covid_analytics.visualization.charts import ChartGenerator
import plotly.express as px

gen = ChartGenerator(data)
fig = gen.create_timeline(
    countries=["France", "Germany"],
    metric="total_cases"
)
fig.show()
```

**New code**:
```python
from epi_analytics import visualize

fig = visualize(
    data,
    chart_type="timeline",
    countries=["France", "Germany"],
    metric="total_cases"
)
fig.show()
```

## Complete Example Migration

### Before (Old Code)

```python
# old_analysis.py
import sys
import os
sys.path.append('scripts')

from data_loader import load_covid_data
from data_cleaner import clean_covid_data
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.visualization.charts import ChartGenerator
from covid_analytics.core.config import Settings

# Load data
settings = Settings()
df = load_covid_data("data/raw/covid_data.csv")
df = clean_covid_data(df)

# Filter to France
france_data = df[df['location'] == 'France']

# Calculate metrics
calc = MetricsCalculator(france_data, settings)
mortality = calc.calculate_mortality_rate()
growth = calc.calculate_growth_rate(window=7)

# Visualize
gen = ChartGenerator(france_data, settings)
fig = gen.create_timeline(metric="total_cases")
fig.show()

print(f"France Mortality: {mortality:.2f}%")
print(f"France Growth Rate: {growth:.2f}%")
```

### After (New Code)

```python
# new_analysis.py
from epi_analytics import load_data, analyze, visualize

# Load data (auto-downloads and caches)
data = load_data()

# Calculate metrics for France
mortality = analyze(data, metric="mortality", country="France")
growth = analyze(data, metric="growth", country="France")

# Visualize
fig = visualize(data, chart_type="timeline", countries=["France"], metric="total_cases")
fig.show()

print(f"France Mortality: {mortality:.2f}%")
print(f"France Growth Rate: {growth:.2f}%")
```

**Result**: 20 lines → 10 lines, zero configuration!

## Breaking Changes

### Removed Features

These features from the old version are **not available** in v0.5.0-beta:

1. **PDF Report Generation** - Not implemented yet
2. **Streamlit Dashboard** - Moved to separate example
3. **Configuration Files** - No longer needed (zero config)
4. **Multiple Data Sources** - Only OWID for now
5. **Advanced ML Models** - Not in beta version

### Changed Behavior

1. **Data Caching**: Now automatic with 24h TTL (was configurable)
2. **Error Handling**: Falls back to sample data instead of crashing
3. **Date Filtering**: Now done via pandas after loading (was in loader)

## Troubleshooting

### "Module not found: epi_analytics"

**Problem**: Old import paths  
**Solution**: Update to new imports:
```python
from epi_analytics import load_data, analyze, visualize
```

### "Cannot find data file"

**Problem**: Looking for old data paths  
**Solution**: Use `load_data()` which auto-downloads:
```python
data = load_data()  # No file path needed
```

### "Settings object not found"

**Problem**: Old configuration system  
**Solution**: No configuration needed anymore! Just use functions directly.

### "My custom analysis doesn't work"

**Problem**: Custom code built on old architecture  
**Solution**: Access the raw DataFrame and use pandas:
```python
data = load_data()
# Now use pandas directly
custom_result = data.groupby('location')['total_cases'].sum()
```

## Getting Help

- **Documentation**: See [GETTING_STARTED.md](GETTING_STARTED_NEW.md)
- **Examples**: Check `examples_new/` folder
- **Issues**: Open a GitHub issue
- **Questions**: GitHub Discussions

## Timeline

- **v0.5.0-beta** (Current): Core functionality, educational focus
- **v0.8.0-rc** (Q2 2026): Additional features, more diseases
- **v1.0.0** (Q3 2026): Production-ready, full feature set

## Feedback

We want to hear from you! If this migration guide is unclear or you encounter issues, please:

1. Open a GitHub issue
2. Suggest improvements to this guide
3. Share your migration experience

Thank you for migrating to Epi Analytics! 🎉
