"""
COVID Analytics - Streamlit Dashboard
Demonstrates the covid-analytics library with an interactive dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import the library
from covid_analytics.data.sources import DataSource
from covid_analytics.processing.cleaners import DataCleaner
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector

# Page config
st.set_page_config(
    page_title="COVID Analytics Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_data(use_cache=True):
    """Load and clean COVID data"""
    with st.spinner("Loading data..."):
        # Load data
        data = DataSource.from_owid(cache=use_cache)
        
        # Clean data
        cleaner = DataCleaner()
        clean_data = cleaner.clean(data)
        
    return clean_data


def main():
    # Header
    st.markdown('<h1 class="main-header">🦠 COVID-19 Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Configuration")
    
    # Data loading options
    st.sidebar.subheader("Data Source")
    use_cache = st.sidebar.checkbox("Use cached data", value=True)
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Load data
    try:
        data = load_data(use_cache)
        
        # Get available countries
        countries = sorted(data['location'].unique().tolist())
        
        # Country selection
        st.sidebar.subheader("Country Selection")
        selected_countries = st.sidebar.multiselect(
            "Select countries to compare",
            countries,
            default=["France", "Germany", "Italy", "Spain", "United Kingdom"][:min(5, len(countries))]
        )
        
        if not selected_countries:
            st.warning("Please select at least one country")
            return
        
        # Date range
        st.sidebar.subheader("Date Range")
        min_date = pd.to_datetime(data['date']).min()
        max_date = pd.to_datetime(data['date']).max()
        
        date_range = st.sidebar.date_input(
            "Select date range",
            value=(max_date - timedelta(days=365), max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Filter data
        filtered_data = data[
            (data['location'].isin(selected_countries)) &
            (pd.to_datetime(data['date']) >= pd.to_datetime(date_range[0])) &
            (pd.to_datetime(data['date']) <= pd.to_datetime(date_range[1]))
        ].copy()
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🔍 Analytics", "ℹ️ About"])
        
        with tab1:
            show_overview(filtered_data, selected_countries)
        
        with tab2:
            show_trends(filtered_data, selected_countries)
        
        with tab3:
            show_analytics(filtered_data, selected_countries)
        
        with tab4:
            show_about()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Try using synthetic data or check your internet connection")


def show_overview(data, countries):
    """Show overview metrics"""
    st.header("📊 Overview")
    
    # Calculate metrics for each country
    metrics_calc = MetricsCalculator(data)
    
    # Display metrics in columns
    cols = st.columns(len(countries))
    
    for idx, country in enumerate(countries):
        with cols[idx]:
            st.subheader(country)
            
            country_data = data[data['location'] == country]
            
            if len(country_data) > 0:
                latest = country_data.iloc[-1]
                
                st.metric(
                    "Total Cases",
                    f"{latest.get('total_cases', 0):,.0f}" if pd.notna(latest.get('total_cases')) else "N/A"
                )
                st.metric(
                    "Total Deaths",
                    f"{latest.get('total_deaths', 0):,.0f}" if pd.notna(latest.get('total_deaths')) else "N/A"
                )
                
                # Mortality rate
                mortality = metrics_calc.mortality_rate(country=country)
                st.metric("Mortality Rate", f"{mortality:.2f}%")
    
    st.markdown("---")
    
    # Cases over time
    st.subheader("Cases Over Time")
    
    fig = px.line(
        data,
        x='date',
        y='total_cases',
        color='location',
        title="Total COVID-19 Cases by Country",
        labels={'total_cases': 'Total Cases', 'date': 'Date', 'location': 'Country'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Deaths over time
    st.subheader("Deaths Over Time")
    
    fig = px.line(
        data,
        x='date',
        y='total_deaths',
        color='location',
        title="Total COVID-19 Deaths by Country",
        labels={'total_deaths': 'Total Deaths', 'date': 'Date', 'location': 'Country'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


def show_trends(data, countries):
    """Show trend analysis"""
    st.header("📈 Trend Analysis")
    
    # Trend detector
    detector = TrendDetector(data)
    
    # Select metric
    metric = st.selectbox(
        "Select metric to analyze",
        ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
    )
    
    # Window size
    window = st.slider("Rolling window (days)", 1, 30, 7)
    
    # Trend summaries
    st.subheader("Current Trends")
    
    cols = st.columns(len(countries))
    
    for idx, country in enumerate(countries):
        with cols[idx]:
            summary = detector.get_trend_summary(
                metric=metric,
                country=country,
                window=window
            )
            
            trend_emoji = {
                "increasing": "📈",
                "decreasing": "📉",
                "stable": "➡️",
                "unknown": "❓"
            }
            
            st.markdown(f"### {country}")
            st.markdown(f"{trend_emoji.get(summary['trend'], '❓')} **{summary['trend'].upper()}**")
            st.markdown(f"Change: **{summary['change']:.1f}%**")
            st.markdown(f"Current: **{summary['current_value']:,.0f}**")
    
    st.markdown("---")
    
    # Trend visualization
    st.subheader("Trend Visualization")
    
    for country in countries:
        trends = detector.detect(
            metric=metric,
            country=country,
            window=window,
            threshold=0.1
        )
        
        if len(trends) > 0:
            fig = go.Figure()
            
            # Original data
            fig.add_trace(go.Scatter(
                x=trends['date'],
                y=trends[metric],
                name=f'{country} - Original',
                line=dict(color='lightgray', width=1)
            ))
            
            # Rolling average
            fig.add_trace(go.Scatter(
                x=trends['date'],
                y=trends['rolling_avg'],
                name=f'{country} - Rolling Avg',
                line=dict(color='blue', width=2)
            ))
            
            fig.update_layout(
                title=f"{country} - {metric.replace('_', ' ').title()}",
                xaxis_title="Date",
                yaxis_title=metric.replace('_', ' ').title(),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)


def show_analytics(data, countries):
    """Show advanced analytics"""
    st.header("🔍 Advanced Analytics")
    
    metrics_calc = MetricsCalculator(data)
    
    # Comparison table
    st.subheader("Country Comparison")
    
    comparison_data = []
    
    for country in countries:
        mortality = metrics_calc.mortality_rate(country=country)
        cfr = metrics_calc.case_fatality_rate(country=country)
        
        country_data = data[data['location'] == country]
        if len(country_data) > 0:
            latest = country_data.iloc[-1]
            
            comparison_data.append({
                'Country': country,
                'Total Cases': f"{latest.get('total_cases', 0):,.0f}" if pd.notna(latest.get('total_cases')) else "N/A",
                'Total Deaths': f"{latest.get('total_deaths', 0):,.0f}" if pd.notna(latest.get('total_deaths')) else "N/A",
                'Mortality Rate (%)': f"{mortality:.2f}",
                'CFR (%)': f"{cfr:.2f}"
            })
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
    
    st.markdown("---")
    
    # Growth rate analysis
    st.subheader("Growth Rate Analysis")
    
    metric_for_growth = st.selectbox(
        "Select metric",
        ['total_cases', 'total_deaths'],
        key="growth_metric"
    )
    
    window_growth = st.slider("Window (days)", 1, 30, 7, key="growth_window")
    
    for country in countries:
        growth = metrics_calc.growth_rate(
            metric=metric_for_growth,
            country=country,
            window=window_growth
        )
        
        if len(growth) > 0:
            country_data = data[data['location'] == country].copy()
            country_data['growth_rate'] = growth
            
            fig = px.line(
                country_data,
                x='date',
                y='growth_rate',
                title=f"{country} - Growth Rate ({metric_for_growth})",
                labels={'growth_rate': 'Growth Rate (%)', 'date': 'Date'}
            )
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.update_layout(height=300)
            
            st.plotly_chart(fig, use_container_width=True)


def show_about():
    """Show about information"""
    st.header("ℹ️ About")
    
    st.markdown("""
    ### COVID Analytics Dashboard
    
    This dashboard demonstrates the **covid-analytics** library, a professional Python library
    for COVID-19 data analysis.
    
    #### Features
    - 📊 Real-time data from Our World in Data
    - 🧹 Automatic data cleaning and validation
    - 📈 Trend detection and analysis
    - 🔍 Advanced analytics (mortality rate, CFR, growth rate)
    - 🎨 Interactive visualizations
    
    #### Technology Stack
    - **Backend**: covid-analytics library
    - **Frontend**: Streamlit
    - **Visualizations**: Plotly
    - **Data**: Our World in Data API
    
    #### Source Code
    This dashboard is part of the covid-analytics library examples.
    
    For more information, visit the [GitHub repository](https://github.com/your-repo/covid-analytics).
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: 2026-01-14
    """)


if __name__ == "__main__":
    main()
