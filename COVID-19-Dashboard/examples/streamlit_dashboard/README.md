# COVID Analytics - Streamlit Dashboard

Interactive dashboard demonstrating the covid-analytics library.

## Features

- 📊 Real-time COVID-19 data visualization
- 📈 Trend analysis with rolling averages
- 🔍 Advanced analytics (mortality rate, CFR, growth rate)
- 🌍 Multi-country comparison
- 🎨 Interactive Plotly charts

## Installation

```bash
# Install the library with Streamlit support
pip install -e ".[streamlit]"
```

## Usage

```bash
# Run the dashboard
streamlit run examples/streamlit_dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## Screenshots

### Overview Tab
- Total cases and deaths by country
- Time series visualizations

### Trends Tab
- Trend detection (increasing/decreasing/stable)
- Rolling averages
- Percentage change analysis

### Analytics Tab
- Country comparison table
- Growth rate analysis
- Advanced metrics

## Configuration

The dashboard uses the covid-analytics library configuration from `.env` file.
See `.env.example` for available options.

## Data Source

Data is automatically fetched from [Our World in Data](https://ourworldindata.org/coronavirus)
and cached locally for performance.
