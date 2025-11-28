"""
Example usage of the Satellite Data Processor V2

This script demonstrates how to use the data processing module
to analyze a flood event and calculate recovery metrics.
"""

from satellite_data_processor_v2 import SatelliteDataProcessor
from datetime import datetime

def main():
    print("=" * 60)
    print("Example: Processing a Flood Event")
    print("=" * 60)
    
    # Initialize the processor
    processor = SatelliteDataProcessor()
    
    # Define a flood event date
    flood_date = datetime(2023, 6, 15)
    print(f"\nProcessing flood event from: {flood_date.strftime('%Y-%m-%d')}")
    
    # Process the flood event with 10 time steps
    results = processor.process_flood_event(flood_date, num_time_steps=10)
    
    # Display key results
    print("\n" + "=" * 60)
    print("Recovery Metrics Summary")
    print("=" * 60)
    
    metrics = results['recovery_metrics']
    print(f"Recovery Percentage: {metrics['recovery_percentage']:.2f}%")
    print(f"Recovery Rate: {metrics['recovery_rate']:.6f}")
    
    if metrics['time_to_recovery_days']:
        print(f"Estimated Time to Recovery: {metrics['time_to_recovery_days']:.1f} days")
    else:
        print("Estimated Time to Recovery: Already recovered or insufficient data")
    
    print(f"Current NDVI: {metrics['current_ndvi']:.3f}")
    print(f"Baseline NDVI: {metrics['baseline_ndvi']:.3f}")
    
    # Display time series summary
    print("\n" + "=" * 60)
    print("Time Series Summary")
    print("=" * 60)
    print(f"Number of time steps: {len(results['time_series'])}")
    print(f"Date range: {results['dates'][0].strftime('%Y-%m-%d')} to {results['dates'][-1].strftime('%Y-%m-%d')}")
    
    print("\nFirst few time steps:")
    print(results['time_series'].head())
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

