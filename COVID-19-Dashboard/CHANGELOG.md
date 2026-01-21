# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-14

### Added
- **Complete project refactoring** from monolithic dashboard to professional Python library
- **Core infrastructure**:
  - Centralized configuration with Pydantic Settings
  - Structured logging with structlog (JSON output)
  - Custom exception hierarchy
  - Pydantic schemas for data validation
- **Data layer**:
  - Our World in Data API integration with automatic caching
  - Smart cache with configurable TTL
  - Fallback to backup URL on primary failure
  - Synthetic data generation for testing
  - Data loader with validation
- **Processing layer**:
  - Comprehensive data cleaning pipeline
  - Duplicate removal
  - Missing value handling (interpolation, filling)
  - Data type conversion and validation
  - Data transformers for derived metrics
- **Analytics layer**:
  - Metrics calculator (mortality rate, CFR, growth rate)
  - Trend detector (increasing/decreasing/stable)
  - Peak detection
  - Anomaly detection (z-score method)
  - Country comparisons
- **Testing infrastructure**:
  - 25+ unit tests with >70% coverage
  - GitHub Actions CI/CD for automated testing
  - Tests for all core modules
- **Documentation**:
  - Professional README with examples
  - Comprehensive docstrings (Google style)
  - Type hints throughout
  - Example applications

### Changed
- **Architecture**: Transformed from monolithic to clean layered architecture
- **Configuration**: Moved from hardcoded paths to centralized Pydantic Settings
- **Logging**: Replaced print() statements with structured logging

### Removed
- **Duplicate files**: Removed main.py, auto_run.py, download_from_github_v2.py
- **God object**: Eliminated data_utils.py (782 lines of duplication)
- **Unused dependencies**: Removed jupyter, scipy from core requirements

### Fixed
- **Code duplication**: Eliminated 100% of duplicate code
- **Missing tests**: Added comprehensive test suite
- **Configuration issues**: Centralized all configuration
- **Logging chaos**: Implemented structured logging

## [0.1.0] - 2020-03-01 (Original Version)

### Added
- Initial COVID-19 Dashboard with Streamlit
- Basic data loading and visualization
- PDF report generation

---

## Upgrade Guide

### From 0.x to 1.0

The 1.0 release is a **complete rewrite** with breaking changes. The project is now a library instead of a standalone dashboard.

**Old usage** (0.x):
```python
from scripts.data_loader import load_covid_data
df = load_covid_data("data/raw/covid_data.csv")
```

**New usage** (1.0+):
```python
from covid_analytics import DataSource, Analytics
data = DataSource.from_owid(cache=True)
analytics = Analytics(data)
```

**Migration steps**:
1. Install the new version: `pip install covid-analytics`
2. Update imports to use the new API
3. Replace hardcoded paths with DataSource methods
4. Use Analytics class for calculations instead of custom functions

For detailed migration guide, see [MIGRATION.md](MIGRATION.md).
