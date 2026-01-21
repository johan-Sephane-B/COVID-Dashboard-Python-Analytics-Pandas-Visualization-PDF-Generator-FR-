# Deployment Instructions - Epi Analytics v0.5.0-beta

## Prerequisites

- Python 3.9+
- Git
- PyPI account (for publishing)
- GitHub account (for CI/CD)

## Step-by-Step Deployment

### Phase 1: Preparation (1-2 hours)

#### 1.1 Reorganize Project Structure

```bash
# Navigate to project root
cd COVID-19-Dashboard

# Create new structure (files already created in src_new/)
# Move files from src_new/ to src/
rm -rf src/covid_analytics  # Remove old code
mv src_new/epi_analytics src/  # Move new code

# Move documentation
mv README_NEW.md README.md
mv GETTING_STARTED_NEW.md GETTING_STARTED.md
mv pyproject_NEW.toml pyproject.toml

# Move examples
rm -rf examples  # Remove old examples
mv examples_new examples

# Move tests
rm -rf tests  # Remove old tests
mv tests_new tests

# Move CI/CD
rm -rf .github
mv .github_new .github
```

#### 1.2 Create Sample Data

```python
# Run this script to create sample data
import pandas as pd
import requests
from pathlib import Path

# Download OWID data
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Select 5 representative countries
countries = ["France", "Germany", "Italy", "Spain", "United Kingdom"]
sample = df[df['location'].isin(countries)]

# Take last 200 days of data
sample = sample.groupby('location').tail(200)

# Save to data/sample/
output_dir = Path("data/sample")
output_dir.mkdir(parents=True, exist_ok=True)
sample.to_csv(output_dir / "covid_sample.csv", index=False)

print(f"✅ Created sample data: {len(sample)} rows, {len(sample['location'].unique())} countries")
```

#### 1.3 Clean Up Old Files

```bash
# Remove old legacy code
rm -rf scripts/
rm app.py
rm -rf pages/
rm requirements_updated.txt
rm fix_imports.py
rm check_structure.*
```

### Phase 2: Testing (2-3 hours)

#### 2.1 Run Tests Locally

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=epi_analytics --cov-report=html

# Open coverage report
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

**Expected**: 85%+ coverage, all tests passing

#### 2.2 Test on Clean Virtual Environment

```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install from local
pip install -e .

# Test imports
python -c "from epi_analytics import load_data, analyze, visualize; print('✅ Imports work')"

# Test functionality
python examples/simple_example.py

# Deactivate
deactivate
```

#### 2.3 Test on Different OS (if possible)

- Windows: Test installation and examples
- Linux: Test installation and examples
- macOS: Test installation and examples

### Phase 3: Build and Publish to TestPyPI (1 hour)

#### 3.1 Build Package

```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# Verify build
ls dist/
# Should see: epi_analytics-0.5.0b0-py3-none-any.whl and .tar.gz
```

#### 3.2 Check Package

```bash
# Verify package
twine check dist/*

# Should output: Checking dist/... PASSED
```

#### 3.3 Upload to TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your TestPyPI API token>
```

#### 3.4 Test Installation from TestPyPI

```bash
# Create fresh environment
python -m venv testpypi_env
source testpypi_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ epi-analytics

# Test
python -c "from epi_analytics import load_data; data = load_data(); print(f'✅ Loaded {len(data)} rows')"

# Deactivate
deactivate
```

### Phase 4: Publish to PyPI (30 minutes)

#### 4.1 Final Checks

- [ ] All tests passing
- [ ] TestPyPI installation works
- [ ] Examples run successfully
- [ ] Documentation is complete
- [ ] CHANGELOG.md is updated
- [ ] Version number is correct (0.5.0-beta)

#### 4.2 Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your PyPI API token>
```

#### 4.3 Verify on PyPI

1. Visit https://pypi.org/project/epi-analytics/
2. Check that page looks correct
3. Test installation:

```bash
pip install epi-analytics
python -c "from epi_analytics import load_data; print('✅ Works')"
```

### Phase 5: GitHub Release (30 minutes)

#### 5.1 Create Git Tag

```bash
# Commit all changes
git add .
git commit -m "Release v0.5.0-beta"

# Create tag
git tag -a v0.5.0-beta -m "Release v0.5.0-beta - Educational epidemiology toolkit"

# Push tag
git push origin v0.5.0-beta
```

#### 5.2 Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Select tag: v0.5.0-beta
4. Release title: "Epi Analytics v0.5.0-beta"
5. Description:

```markdown
## Epi Analytics v0.5.0-beta

Educational Python toolkit for epidemiological data analysis.

### Features
- 📊 Auto-download COVID-19 data from Our World in Data
- 🧮 Simple API: `load_data`, `analyze`, `visualize`
- 📈 Interactive Plotly charts
- 🎓 Perfect for students and educators

### Installation
```bash
pip install epi-analytics
```

### Quick Start
```python
from epi_analytics import load_data, analyze, visualize

data = load_data()
mortality = analyze(data, metric="mortality", country="France")
print(f"Mortality: {mortality:.2%}")
```

### Documentation
- [Getting Started](GETTING_STARTED.md)
- [Examples](examples/)
- [Migration Guide](MIGRATION_GUIDE.md)

### What's New
- Complete rewrite from COVID-Dashboard
- Simplified API (3 functions vs 20+)
- 75% less code
- Zero configuration required
- Auto-download and caching

### Known Limitations
- Beta version - not production-ready
- Only COVID-19 data supported
- No PDF generation yet

### Next Steps
- v0.8.0-rc: Additional diseases, more metrics
- v1.0.0: Production-ready, full feature set
```

6. Attach files: dist/*.whl and dist/*.tar.gz
7. Check "This is a pre-release" (since it's beta)
8. Click "Publish release"

### Phase 6: Announcements (1-2 hours)

#### 6.1 Reddit Posts

**r/Python**:
```
Title: [Project] Epi Analytics - Learn epidemiology with Python

I've released Epi Analytics v0.5.0-beta, an educational Python library for analyzing pandemic data.

Perfect for students learning data science or anyone interested in epidemiology.

Features:
- Auto-download COVID-19 data
- Simple 3-function API
- Interactive visualizations
- Works in Google Colab

pip install epi-analytics

GitHub: [link]
Docs: [link]

Feedback welcome!
```

**r/datascience**:
```
Title: New educational tool for epidemiological data analysis

Released Epi Analytics - a Python library for learning pandemic data analysis.

Great for:
- Data science students
- Educators teaching time series analysis
- Anyone learning Pandas/Plotly

3-function API makes it easy to get started in 5 minutes.

[link to repo]
```

#### 6.2 Twitter/X

```
🚀 Just released Epi Analytics v0.5.0-beta!

📊 Educational Python toolkit for pandemic data analysis
🎓 Perfect for students & educators
⚡ 3-function API: load, analyze, visualize

pip install epi-analytics

#Python #DataScience #Epidemiology

[link]
```

#### 6.3 Email to Educators

Template:
```
Subject: New Educational Tool - Epi Analytics for Python

Dear [Professor Name],

I've developed an educational Python library called Epi Analytics that might be useful for your data science courses.

It simplifies epidemiological data analysis with a 3-function API, making it perfect for students learning:
- Time series analysis
- Data visualization
- Real-world data science

Key features:
- Auto-downloads COVID-19 data
- Works in Google Colab (no setup)
- Interactive Plotly visualizations
- Comprehensive documentation

Installation: pip install epi-analytics
Documentation: [link]
Examples: [link to Colab notebook]

I'd love to hear your feedback if you try it in your courses.

Best regards,
[Your Name]
```

Send to 5-10 professors teaching data science.

### Phase 7: Monitoring (Ongoing)

#### 7.1 Set Up Monitoring

- **PyPI Stats**: Check https://pypistats.org/packages/epi-analytics daily
- **GitHub**: Monitor stars, issues, PRs
- **Google Alerts**: Set alert for "epi-analytics python"

#### 7.2 Response Plan

- **Issues**: Respond within 24 hours
- **PRs**: Review within 48 hours
- **Questions**: Answer on GitHub Discussions

#### 7.3 Weekly Review

Every Monday:
1. Check download stats
2. Review open issues
3. Update roadmap if needed
4. Plan next week's work

## Rollback Plan

If critical issues are discovered:

```bash
# 1. Yank the release from PyPI
# (Go to PyPI project page → Manage → Yank release)

# 2. Create hotfix
git checkout -b hotfix/v0.5.1-beta

# 3. Fix issue, test thoroughly

# 4. Release v0.5.1-beta following steps above
```

## Success Metrics

Track these weekly:

| Metric | Week 1 | Week 2 | Week 4 | Target (3 months) |
|--------|--------|--------|--------|-------------------|
| Downloads | 50+ | 100+ | 200+ | 1,000+ |
| GitHub Stars | 10+ | 20+ | 50+ | 100+ |
| Issues Opened | 2-5 | 3-7 | 5-10 | - |
| Issues Resolved | 100% | 95%+ | 95%+ | 95%+ |

## Troubleshooting

### Build Fails

```bash
# Check pyproject.toml syntax
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"

# Verify package structure
python -m build --sdist --wheel --outdir dist/ .
```

### Upload Fails

```bash
# Check credentials
twine check dist/*

# Verify API token is correct
# Regenerate token if needed
```

### Installation Fails

```bash
# Test locally first
pip install -e .

# Check dependencies
pip install pandas numpy requests plotly
```

## Next Steps After Deployment

1. **Week 1**: Monitor closely, fix critical bugs
2. **Week 2-4**: Gather feedback, plan v0.6
3. **Month 2-3**: Implement requested features
4. **Month 4**: Prepare v0.8.0-rc

## Checklist

- [ ] Sample data created
- [ ] Old files removed
- [ ] Tests passing (85%+ coverage)
- [ ] Tested on clean environment
- [ ] Published to TestPyPI
- [ ] Tested TestPyPI installation
- [ ] Published to PyPI
- [ ] GitHub release created
- [ ] Announcements posted
- [ ] Monitoring set up

---

**Good luck with the deployment! 🚀**
