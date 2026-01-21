"""
Performance benchmarks for covid-analytics library
Validates performance claims and identifies bottlenecks
"""

import time
import pandas as pd
import numpy as np
from memory_profiler import memory_usage
import sys

from covid_analytics.data.sources import DataSource
from covid_analytics.processing.cleaners import DataCleaner
from covid_analytics.analytics.metrics import MetricsCalculator
from covid_analytics.analytics.trends import TrendDetector


def benchmark_data_loading():
    """Benchmark data loading performance"""
    print("\n" + "="*60)
    print("BENCHMARK 1: Data Loading")
    print("="*60)
    
    # Test 1: Load from OWID (first time, no cache)
    print("\n📥 Test 1.1: Load from OWID (no cache)")
    start = time.time()
    data = DataSource.from_owid(cache=False)
    duration = time.time() - start
    print(f"   Time: {duration:.2f}s")
    print(f"   Rows: {len(data):,}")
    print(f"   Throughput: {len(data)/duration:,.0f} rows/sec")
    
    # Test 2: Load from cache
    print("\n📥 Test 1.2: Load from cache")
    start = time.time()
    data_cached = DataSource.from_owid(cache=True)
    duration_cached = time.time() - start
    print(f"   Time: {duration_cached:.2f}s")
    print(f"   Speedup: {duration/duration_cached:.1f}x faster")
    
    # Test 3: Synthetic data generation
    print("\n📥 Test 1.3: Generate synthetic data")
    start = time.time()
    synthetic = DataSource.synthetic(countries=10, days=365)
    duration_synthetic = time.time() - start
    print(f"   Time: {duration_synthetic:.2f}s")
    print(f"   Rows: {len(synthetic):,}")
    
    return data


def benchmark_data_cleaning(data):
    """Benchmark data cleaning performance"""
    print("\n" + "="*60)
    print("BENCHMARK 2: Data Cleaning")
    print("="*60)
    
    cleaner = DataCleaner()
    
    # Test with different data sizes
    sizes = [1000, 10000, 100000, len(data)]
    
    for size in sizes:
        sample = data.head(size).copy()
        
        print(f"\n🧹 Test 2.{sizes.index(size)+1}: Clean {size:,} rows")
        start = time.time()
        clean = cleaner.clean(sample)
        duration = time.time() - start
        
        print(f"   Time: {duration:.3f}s")
        print(f"   Throughput: {size/duration:,.0f} rows/sec")
        print(f"   Removed: {len(sample) - len(clean):,} rows")
    
    return cleaner.clean(data)


def benchmark_analytics(data):
    """Benchmark analytics performance"""
    print("\n" + "="*60)
    print("BENCHMARK 3: Analytics")
    print("="*60)
    
    metrics = MetricsCalculator(data)
    
    # Test 1: Mortality rate calculation
    print("\n📊 Test 3.1: Mortality rate calculation")
    countries = data['location'].unique()[:10]
    
    start = time.time()
    for country in countries:
        _ = metrics.mortality_rate(country=country)
    duration = time.time() - start
    
    print(f"   Countries: {len(countries)}")
    print(f"   Time: {duration:.3f}s")
    print(f"   Avg per country: {duration/len(countries)*1000:.1f}ms")
    
    # Test 2: Growth rate calculation
    print("\n📊 Test 3.2: Growth rate calculation")
    start = time.time()
    growth = metrics.growth_rate(metric="total_cases", country=countries[0], window=7)
    duration = time.time() - start
    
    print(f"   Time: {duration:.3f}s")
    print(f"   Points: {len(growth):,}")
    
    # Test 3: Trend detection
    print("\n📊 Test 3.3: Trend detection")
    detector = TrendDetector(data)
    
    start = time.time()
    for country in countries:
        _ = detector.get_trend_summary(metric="total_cases", country=country)
    duration = time.time() - start
    
    print(f"   Countries: {len(countries)}")
    print(f"   Time: {duration:.3f}s")
    print(f"   Avg per country: {duration/len(countries)*1000:.1f}ms")


def benchmark_memory():
    """Benchmark memory usage"""
    print("\n" + "="*60)
    print("BENCHMARK 4: Memory Usage")
    print("="*60)
    
    def load_and_process():
        data = DataSource.from_owid(cache=True)
        cleaner = DataCleaner()
        clean = cleaner.clean(data)
        metrics = MetricsCalculator(clean)
        _ = metrics.mortality_rate(country="France")
        return clean
    
    print("\n💾 Measuring memory usage...")
    mem_usage = memory_usage(load_and_process, interval=0.1)
    
    print(f"   Peak memory: {max(mem_usage):.1f} MB")
    print(f"   Baseline: {min(mem_usage):.1f} MB")
    print(f"   Delta: {max(mem_usage) - min(mem_usage):.1f} MB")


def benchmark_scalability():
    """Benchmark scalability with large datasets"""
    print("\n" + "="*60)
    print("BENCHMARK 5: Scalability")
    print("="*60)
    
    sizes = [10000, 50000, 100000, 500000, 1000000]
    
    for size in sizes:
        print(f"\n📈 Test 5.{sizes.index(size)+1}: {size:,} rows")
        
        # Generate synthetic data
        countries = max(10, size // 365)
        days = min(365, size // countries)
        data = DataSource.synthetic(countries=countries, days=days, seed=42)
        
        # Ensure we have the right size
        data = data.head(size)
        
        # Test cleaning
        cleaner = DataCleaner()
        start = time.time()
        clean = cleaner.clean(data)
        clean_time = time.time() - start
        
        # Test analytics
        metrics = MetricsCalculator(clean)
        start = time.time()
        _ = metrics.mortality_rate(country=clean['location'].iloc[0])
        analytics_time = time.time() - start
        
        total_time = clean_time + analytics_time
        
        print(f"   Clean: {clean_time:.3f}s ({size/clean_time:,.0f} rows/sec)")
        print(f"   Analytics: {analytics_time:.3f}s")
        print(f"   Total: {total_time:.3f}s")
        
        # Check if we meet the <500ms target for 1M rows
        if size == 1000000:
            if total_time < 0.5:
                print(f"   ✅ PASSED: {total_time:.3f}s < 0.5s target")
            else:
                print(f"   ⚠️ MISSED: {total_time:.3f}s > 0.5s target")


def main():
    """Run all benchmarks"""
    print("\n" + "="*60)
    print("COVID ANALYTICS - PERFORMANCE BENCHMARKS")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"Pandas: {pd.__version__}")
    print(f"NumPy: {np.__version__}")
    
    try:
        # Run benchmarks
        data = benchmark_data_loading()
        clean_data = benchmark_data_cleaning(data)
        benchmark_analytics(clean_data)
        
        try:
            benchmark_memory()
        except ImportError:
            print("\n⚠️ Skipping memory benchmark (install memory_profiler)")
        
        benchmark_scalability()
        
        print("\n" + "="*60)
        print("✅ ALL BENCHMARKS COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
