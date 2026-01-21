"""
Simple example: Analyze COVID-19 mortality rates

This 10-line script demonstrates the core functionality of epi-analytics.
"""

from epi_analytics import load_data, analyze, visualize

# Load data (auto-downloads and caches)
data = load_data()

# Analyze mortality for top 5 countries by cases
top_countries = data.groupby('location')['total_cases'].max().nlargest(5).index.tolist()

for country in top_countries:
    mortality = analyze(data, metric="mortality", country=country)
    print(f"{country:20s}: {mortality:.2f}% mortality rate")

# Visualize timeline
fig = visualize(data, chart_type="timeline", countries=top_countries, metric="total_deaths")
fig.show()
