"""
Satellite Data Processing Module V2
AI-Driven Satellite Platform for Post-Flood Landscape Recovery Analysis

This module implements the second iteration of the data processing pipeline,
including:
- Multi-sensor data loading (Sentinel-1 and Sentinel-2)
- NDVI, NDWI, and radar backscatter calculations
- Time-series analysis
- Recovery metrics computation
"""

import numpy as np
import pandas as pd
import xarray as xr
import rioxarray as rio
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')


class SatelliteDataProcessor:
    """
    Main class for processing satellite data from Sentinel-1 and Sentinel-2.
    Handles data loading, index calculation, and time-series analysis.
    """
    
    def __init__(self, sentinel1_path: Optional[str] = None, 
                 sentinel2_path: Optional[str] = None):
        """
        Initialize the processor.
        
        Args:
            sentinel1_path: Path to Sentinel-1 data (optional, can use simulated data)
            sentinel2_path: Path to Sentinel-2 data (optional, can use simulated data)
        """
        self.sentinel1_path = sentinel1_path
        self.sentinel2_path = sentinel2_path
        self.processed_data = {}
        
    def load_sentinel2_data(self, red_band: Optional[np.ndarray] = None,
                           nir_band: Optional[np.ndarray] = None,
                           swir_band: Optional[np.ndarray] = None,
                           green_band: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
        """
        Load Sentinel-2 optical data.
        
        Args:
            red_band: Red band data (Band 4) - if None, generates simulated data
            nir_band: Near-infrared band data (Band 8) - if None, generates simulated data
            swir_band: SWIR band data (Band 11) - if None, generates simulated data
            green_band: Green band data (Band 3) - if None, generates simulated data
            
        Returns:
            Dictionary containing loaded bands
        """
        if red_band is None or nir_band is None:
            # Generate simulated data for demonstration
            print("Generating simulated Sentinel-2 data...")
            height, width = 500, 500
            red_band = np.random.rand(height, width) * 0.3 + 0.1
            nir_band = np.random.rand(height, width) * 0.4 + 0.3
            swir_band = np.random.rand(height, width) * 0.3 + 0.1
            green_band = np.random.rand(height, width) * 0.3 + 0.1
            
        return {
            'red': red_band,
            'nir': nir_band,
            'swir': swir_band,
            'green': green_band
        }
    
    def load_sentinel1_data(self, vv_band: Optional[np.ndarray] = None,
                           vh_band: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
        """
        Load Sentinel-1 radar data.
        
        Args:
            vv_band: VV polarization backscatter - if None, generates simulated data
            vh_band: VH polarization backscatter - if None, generates simulated data
            
        Returns:
            Dictionary containing loaded radar bands
        """
        if vv_band is None or vh_band is None:
            # Generate simulated data for demonstration
            print("Generating simulated Sentinel-1 data...")
            height, width = 500, 500
            # Radar backscatter typically in dB scale (-30 to 5 dB)
            vv_band = np.random.rand(height, width) * 35 - 30
            vh_band = np.random.rand(height, width) * 35 - 30
            
        return {
            'vv': vv_band,
            'vh': vh_band
        }
    
    def calculate_ndvi(self, red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Vegetation Index (NDVI).
        
        NDVI = (NIR - Red) / (NIR + Red)
        
        Args:
            red_band: Red band reflectance
            nir_band: Near-infrared band reflectance
            
        Returns:
            NDVI array (values between -1 and 1)
        """
        denominator = nir_band + red_band
        # Avoid division by zero
        denominator = np.where(denominator == 0, np.nan, denominator)
        ndvi = (nir_band - red_band) / denominator
        return ndvi
    
    def calculate_ndwi(self, green_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Water Index (NDWI).
        
        NDWI = (Green - NIR) / (Green + NIR)
        
        Args:
            green_band: Green band reflectance
            nir_band: Near-infrared band reflectance
            
        Returns:
            NDWI array (values between -1 and 1)
        """
        denominator = green_band + nir_band
        denominator = np.where(denominator == 0, np.nan, denominator)
        ndwi = (green_band - nir_band) / denominator
        return ndwi
    
    def calculate_radar_backscatter(self, vv_band: np.ndarray, vh_band: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Process radar backscatter data.
        
        Args:
            vv_band: VV polarization backscatter (dB)
            vh_band: VH polarization backscatter (dB)
            
        Returns:
            Dictionary with processed radar metrics
        """
        # Convert from dB to linear scale for some calculations
        vv_linear = 10 ** (vv_band / 10)
        vh_linear = 10 ** (vh_band / 10)
        
        # Calculate cross-ratio (VV/VH)
        cross_ratio = np.where(vh_linear != 0, vv_linear / vh_linear, np.nan)
        
        return {
            'vv_db': vv_band,
            'vh_db': vh_band,
            'vv_linear': vv_linear,
            'vh_linear': vh_linear,
            'cross_ratio': cross_ratio
        }
    
    def process_time_series(self, dates: List[datetime], 
                           ndvi_series: List[np.ndarray],
                           ndwi_series: List[np.ndarray],
                           radar_series: List[Dict[str, np.ndarray]]) -> pd.DataFrame:
        """
        Process time-series data to extract recovery metrics.
        
        Args:
            dates: List of acquisition dates
            ndvi_series: List of NDVI arrays over time
            ndwi_series: List of NDWI arrays over time
            radar_series: List of radar backscatter dictionaries over time
            
        Returns:
            DataFrame with time-series metrics per pixel
        """
        if not dates or not ndvi_series:
            raise ValueError("Time series data cannot be empty")
        
        # For demonstration, create a simplified time-series
        # In production, this would process actual multi-temporal data
        results = []
        
        for i, date in enumerate(dates):
            if i < len(ndvi_series):
                ndvi = ndvi_series[i]
                ndwi = ndwi_series[i] if i < len(ndwi_series) else None
                radar = radar_series[i] if i < len(radar_series) else None
                
                # Calculate statistics for this time step
                mean_ndvi = np.nanmean(ndvi)
                std_ndvi = np.nanstd(ndvi)
                
                result = {
                    'date': date,
                    'mean_ndvi': mean_ndvi,
                    'std_ndvi': std_ndvi,
                    'mean_ndwi': np.nanmean(ndwi) if ndwi is not None else None,
                    'mean_vv_backscatter': np.nanmean(radar['vv_db']) if radar else None
                }
                results.append(result)
        
        return pd.DataFrame(results)
    
    def calculate_recovery_metrics(self, ndvi_time_series: pd.DataFrame,
                                  flood_date: datetime) -> Dict[str, float]:
        """
        Calculate recovery metrics from NDVI time series.
        
        Args:
            ndvi_time_series: DataFrame with NDVI values over time
            flood_date: Date of the flood event
            
        Returns:
            Dictionary with recovery metrics
        """
        # Filter data after flood
        post_flood = ndvi_time_series[ndvi_time_series['date'] >= flood_date]
        
        if len(post_flood) == 0:
            return {
                'recovery_rate': 0.0,
                'time_to_recovery_days': None,
                'recovery_percentage': 0.0
            }
        
        # Calculate recovery rate (slope of NDVI over time)
        if len(post_flood) > 1:
            days_since_flood = [(d - flood_date).days for d in post_flood['date']]
            recovery_rate = np.polyfit(days_since_flood, post_flood['mean_ndvi'], 1)[0]
        else:
            recovery_rate = 0.0
        
        # Estimate time to recovery (simplified - would use survival analysis in production)
        baseline_ndvi = 0.6  # Pre-flood baseline (would be calculated from historical data)
        current_ndvi = post_flood['mean_ndvi'].iloc[-1]
        recovery_percentage = min(100, (current_ndvi / baseline_ndvi) * 100) if baseline_ndvi > 0 else 0
        
        # Estimate days to recovery (linear extrapolation)
        if recovery_rate > 0 and current_ndvi < baseline_ndvi:
            days_to_recovery = (baseline_ndvi - current_ndvi) / recovery_rate
        else:
            days_to_recovery = None
        
        return {
            'recovery_rate': recovery_rate,
            'time_to_recovery_days': days_to_recovery,
            'recovery_percentage': recovery_percentage,
            'current_ndvi': current_ndvi,
            'baseline_ndvi': baseline_ndvi
        }
    
    def process_flood_event(self, flood_date: datetime,
                           num_time_steps: int = 10) -> Dict:
        """
        Main processing function for a flood event.
        
        Args:
            flood_date: Date of the flood event
            num_time_steps: Number of time steps to process
            
        Returns:
            Dictionary with all processed data and metrics
        """
        print(f"Processing flood event from {flood_date}")
        
        # Load Sentinel-2 data
        s2_data = self.load_sentinel2_data()
        
        # Load Sentinel-1 data
        s1_data = self.load_sentinel1_data()
        
        # Calculate indices
        ndvi = self.calculate_ndvi(s2_data['red'], s2_data['nir'])
        ndwi = self.calculate_ndwi(s2_data['green'], s2_data['nir'])
        radar_metrics = self.calculate_radar_backscatter(s1_data['vv'], s1_data['vh'])
        
        # Create time series (simulated)
        dates = [flood_date + timedelta(days=i*30) for i in range(num_time_steps)]
        ndvi_series = [ndvi + np.random.normal(0, 0.05, ndvi.shape) * (i/num_time_steps) 
                      for i in range(num_time_steps)]
        ndwi_series = [ndwi + np.random.normal(0, 0.05, ndwi.shape) * (i/num_time_steps) 
                       for i in range(num_time_steps)]
        radar_series = [radar_metrics for _ in range(num_time_steps)]
        
        # Process time series
        time_series_df = self.process_time_series(dates, ndvi_series, ndwi_series, radar_series)
        
        # Calculate recovery metrics
        recovery_metrics = self.calculate_recovery_metrics(time_series_df, flood_date)
        
        # Store results
        self.processed_data = {
            'ndvi': ndvi,
            'ndwi': ndwi,
            'radar_metrics': radar_metrics,
            'time_series': time_series_df,
            'recovery_metrics': recovery_metrics,
            'dates': dates
        }
        
        print("Processing complete!")
        print(f"Recovery metrics: {recovery_metrics}")
        
        return self.processed_data


def main():
    """
    Main execution function for demonstration.
    """
    print("=" * 60)
    print("Satellite Data Processing Module V2")
    print("Post-Flood Recovery Analysis")
    print("=" * 60)
    
    # Initialize processor
    processor = SatelliteDataProcessor()
    
    # Process a flood event
    flood_date = datetime(2023, 6, 15)
    results = processor.process_flood_event(flood_date, num_time_steps=8)
    
    # Display summary
    print("\n" + "=" * 60)
    print("Processing Summary")
    print("=" * 60)
    print(f"NDVI shape: {results['ndvi'].shape}")
    print(f"NDWI shape: {results['ndwi'].shape}")
    print(f"Time series length: {len(results['time_series'])}")
    print(f"\nRecovery Metrics:")
    for key, value in results['recovery_metrics'].items():
        print(f"  {key}: {value}")
    
    return results


if __name__ == "__main__":
    results = main()

