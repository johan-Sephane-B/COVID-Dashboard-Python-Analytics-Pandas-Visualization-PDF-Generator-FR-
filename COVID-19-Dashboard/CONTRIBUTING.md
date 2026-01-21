# Contributing to COVID Analytics

Thank you for your interest in contributing to COVID Analytics! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include**:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Code samples if applicable

### Suggesting Features

1. **Check existing feature requests** first
2. **Describe the use case** clearly
3. **Explain why** this feature would be valuable
4. **Provide examples** of how it would be used

### Pull Requests

#### Before You Start

1. **Open an issue** to discuss major changes
2. **Check the roadmap** to avoid duplicate work
3. **Fork the repository** and create a branch

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/covid-analytics.git
cd covid-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

#### Code Standards

- **Style**: Follow PEP 8, use `ruff` for linting
- **Type hints**: Add type annotations to all functions
- **Docstrings**: Use Google style docstrings
- **Tests**: Write tests for new features (maintain >70% coverage)
- **Commits**: Use clear, descriptive commit messages

**Example commit message**:
```
Add anomaly detection to TrendDetector

- Implement z-score method for anomaly detection
- Add tests for anomaly detection
- Update documentation
```

#### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=covid_analytics --cov-report=html

# Run specific test file
pytest tests/unit/test_analytics_metrics.py

# Run linting
ruff check src/ tests/
mypy src/
```

#### Pull Request Process

1. **Update tests**: Ensure all tests pass
2. **Update documentation**: Add docstrings and update README if needed
3. **Update CHANGELOG.md**: Add entry under "Unreleased"
4. **Create PR**: Use the PR template
5. **Wait for review**: Address feedback promptly

### Code Review Guidelines

**For reviewers**:
- Be constructive and respectful
- Focus on code quality, not personal preferences
- Suggest improvements, don't just criticize
- Approve when ready, request changes if needed

**For contributors**:
- Respond to feedback promptly
- Don't take criticism personally
- Ask questions if feedback is unclear
- Update PR based on feedback

## Development Guidelines

### Project Structure

```
covid-analytics/
├── src/covid_analytics/    # Main package
│   ├── core/               # Infrastructure
│   ├── data/               # Data access
│   ├── processing/         # Data processing
│   └── analytics/          # Business logic
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── examples/              # Example applications
└── docs/                  # Documentation
```

### Adding a New Feature

1. **Create module** in appropriate layer (data/processing/analytics)
2. **Write tests** first (TDD approach recommended)
3. **Implement feature** with type hints and docstrings
4. **Update `__init__.py`** to export public API
5. **Add example** in examples/ or docstring
6. **Update documentation**

### Writing Tests

```python
"""Tests for new feature"""

import pytest
from covid_analytics import YourFeature


class TestYourFeature:
    """Test YourFeature class"""
    
    def test_basic_functionality(self):
        """Test basic usage"""
        feature = YourFeature()
        result = feature.do_something()
        assert result == expected_value
    
    def test_error_handling(self):
        """Test error cases"""
        feature = YourFeature()
        with pytest.raises(ValueError):
            feature.do_something(invalid_input)
```

### Documentation

- **Docstrings**: Required for all public functions/classes
- **Type hints**: Required for all function signatures
- **Examples**: Include usage examples in docstrings
- **README**: Update if adding user-facing features

**Docstring example**:
```python
def calculate_metric(data: pd.DataFrame, country: str) -> float:
    """
    Calculate metric for a specific country.
    
    Args:
        data: DataFrame with COVID-19 data
        country: Country name to filter
    
    Returns:
        Calculated metric value
    
    Raises:
        ValueError: If country not found in data
    
    Example:
        >>> calc = Calculator(data)
        >>> result = calc.calculate_metric(data, "France")
        >>> print(f"Result: {result:.2f}")
    """
```

## Release Process

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release date
3. **Create git tag**: `git tag v1.0.0`
4. **Push tag**: `git push origin v1.0.0`
5. **GitHub Actions** will automatically publish to PyPI

## Questions?

- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs and feature requests
- **Email**: contact@covid-analytics.org

Thank you for contributing! 🎉
