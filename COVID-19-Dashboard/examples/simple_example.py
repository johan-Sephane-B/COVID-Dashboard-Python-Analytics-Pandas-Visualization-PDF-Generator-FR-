"""
Simple example application using the covid-analytics library.
Demonstrates basic usage of the library.
"""

from covid_analytics import DataSource, Analytics
from covid_analytics.processing import DataCleaner
from covid_analytics.analytics import TrendDetector


def main():
    """Main example function"""
    print("🦠 COVID Analytics Library - Example Usage\n")
    
    # 1. Load data
    print("📥 Loading data...")
    data = DataSource.synthetic(countries=5, days=100, seed=42)
    print(f"✅ Loaded {len(data)} rows\n")
    
    # 2. Clean data
    print("🧹 Cleaning data...")
    cleaner = DataCleaner()
    clean_data = cleaner.clean(data)
    print(f"✅ Cleaned data: {len(clean_data)} rows\n")
    
    # 3. Calculate metrics
    print("📊 Calculating metrics...")
    analytics = Analytics(clean_data)
    
    for country in ["France", "Germany", "Italy"]:
        mortality = analytics.calculate_mortality_rate(country=country)
        print(f"  {country}: Mortality rate = {mortality:.2f}%")
    
    print()
    
    # 4. Detect trends
    print("📈 Detecting trends...")
    detector = TrendDetector(clean_data)
    
    for country in ["France", "Germany"]:
        summary = detector.get_trend_summary(
            metric="total_cases",
            country=country,
            window=7
        )
        print(f"  {country}: {summary['trend']} ({summary['change']:.1f}% change)")
    
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
