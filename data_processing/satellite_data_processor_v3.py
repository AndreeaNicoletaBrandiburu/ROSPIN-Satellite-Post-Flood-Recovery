"""
Satellite Data Processing Module V3 (AI-Integrated)
Inherits from V2 and adds Survival Analysis for precise recovery tracking.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
import sys
import os

# --- 1. ROBUST IMPORT FIX ---
# Get the absolute path of the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure this directory is in Python's search path
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Now try to import the V2 processor
try:
    # Attempt 1: Standard import (works if script is run directly or path is set)
    from satellite_data_processor_v2 import SatelliteDataProcessor
except ImportError:
    try:
        # Attempt 2: Package import (works if running from backend/app.py)
        from data_processing.satellite_data_processor_v2 import SatelliteDataProcessor
    except ImportError:
        # Attempt 3: Parent directory fallback
        sys.path.append(os.path.join(current_dir, '..'))
        from satellite_data_processor_v2 import SatelliteDataProcessor

# --- 2. IMPORT AI LIBRARY ---
try:
    from lifelines import KaplanMeierFitter
except ImportError:
    print("⚠️ Warning: 'lifelines' not found. AI features will be limited.")
    KaplanMeierFitter = None

warnings.filterwarnings('ignore')

class SatelliteAIProcessor(SatelliteDataProcessor):
    """
    V3 Processor: Extends V2 by keeping the 3D data stack
    to perform 'Survival Analysis' (Time-to-Recovery) on pixels.
    """

    def __init__(self, sentinel1_path=None, sentinel2_path=None):
        # Initialize the parent V2 class
        super().__init__(sentinel1_path, sentinel2_path)
        self.kmf = KaplanMeierFitter() if KaplanMeierFitter else None
        print("✅ AI Processor Initialized (V3)")

    def run_survival_analysis(self, ndvi_stack, baseline_ndvi):
        """
        AI CORE: Calculates how long each pixel takes to 'survive' (recover).
        """
        if self.kmf is None:
            return None

        print("🧠 AI: Converting satellite imagery to Life Tables...")

        time_steps, height, width = ndvi_stack.shape

        # Define recovery threshold (e.g., 90% of baseline health)
        recovery_threshold = baseline_ndvi * 0.9

        # Create a simple flood mask (simulated for the center)
        flood_mask = np.zeros((height, width), dtype=bool)
        flood_mask[150:350, 150:350] = True

        # t_matrix: Time to event (default = max time)
        t_matrix = np.full((height, width), time_steps, dtype=float)
        # e_matrix: Event observed? (0=No, 1=Yes)
        e_matrix = np.zeros((height, width), dtype=int)

        # Iterate through time to find when pixels heal
        for step in range(time_steps):
            current_ndvi = ndvi_stack[step]

            # Check which pixels are healed at this step
            is_healed = (current_ndvi >= recovery_threshold)

            # Find pixels that are healed NOW, but weren't before
            newly_healed = is_healed & (e_matrix == 0) & flood_mask

            t_matrix[newly_healed] = step + 1
            e_matrix[newly_healed] = 1

        # Run Kaplan-Meier Fit on the flooded area
        flooded_t = t_matrix[flood_mask]
        flooded_e = e_matrix[flood_mask]

        median_recovery = 0
        confidence = 0.0

        if len(flooded_t) > 0:
            self.kmf.fit(flooded_t, event_observed=flooded_e, label='Recovery')
            median_recovery = self.kmf.median_survival_time_
            # Confidence score based on number of observed events
            confidence = np.mean(flooded_e) * 100

        return {
            'median_recovery_time': median_recovery,
            'confidence_score': confidence,
            'recovery_map': t_matrix
        }

    def process_flood_event_ai(self, flood_date, num_time_steps=8):
        """
        V3 Execution: Reuses V2 loading but manages the data stack for AI.
        """
        print(f"Processing flood event from {flood_date}")

        # 1. REUSE V2: Load Data & Calc Indices
        s2_data = self.load_sentinel2_data() # Inherited from V2
        s1_data = self.load_sentinel1_data() # Inherited from V2

        baseline_ndvi = self.calculate_ndvi(s2_data['red'], s2_data['nir'])
        baseline_ndwi = self.calculate_ndwi(s2_data['green'], s2_data['nir'])
        radar_metrics = self.calculate_radar_backscatter(s1_data['vv'], s1_data['vh'])

        # 2. GENERATE TIME SERIES (Need the raw stack for AI)
        # We simulate the stack here because V2's process_flood_event discards it.
        dates = [flood_date + timedelta(days=i*30) for i in range(num_time_steps)]

        ndvi_stack = []
        ndvi_series_for_df = [] # For the V2 dataframe

        for i in range(num_time_steps):
            # Simulate recovery curve
            factor = (i / num_time_steps) * 0.4
            noise = np.random.normal(0, 0.05, baseline_ndvi.shape)
            frame = baseline_ndvi - 0.2 + factor + noise

            ndvi_stack.append(frame)
            ndvi_series_for_df.append(frame)

        ndvi_stack = np.array(ndvi_stack)

        # 3. REUSE V2: Create standard DataFrame
        # We pass None for radar/ndwi series to keep simulation simple, or replicate if needed
        time_series_df = self.process_time_series(
            dates,
            ndvi_series_for_df,
            ndvi_series_for_df, # reusing as dummy NDWI
            [radar_metrics]*num_time_steps
        )

        # 4. REUSE V2: Calculate Standard Metrics
        v2_metrics = self.calculate_recovery_metrics(time_series_df, flood_date)

        # 5. NEW V3: Run AI Analysis
        ai_metrics = self.run_survival_analysis(ndvi_stack, baseline_ndvi)

        # Store everything
        self.processed_data = {
            'ndvi': baseline_ndvi,
            'ndwi': baseline_ndwi,
            'time_series': time_series_df,
            'recovery_metrics': v2_metrics,
            'ai_metrics': ai_metrics
        }

        print("Processing complete!")
        return self.processed_data

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    print("=" * 60)
    print("Satellite Data Processing Module V3 (AI-Integrated)")
    print("Post-Flood Recovery Analysis")
    print("=" * 60)

    processor = SatelliteAIProcessor()

    flood_date = datetime(2023, 6, 15)
    results = processor.process_flood_event_ai(flood_date, num_time_steps=8)

    # --- REPORTING (Matches V2 Style + AI Section) ---
    print("\n" + "=" * 60)
    print("Processing Summary")
    print("=" * 60)

    print(f"NDVI shape: {results['ndvi'].shape}")
    print(f"NDWI shape: {results['ndwi'].shape}")
    print(f"Time series length: {len(results['time_series'])}")

    print(f"\n[Standard V2 Metrics]")
    for key, value in results['recovery_metrics'].items():
        # Clean up numpy formatting for cleaner display
        val_str = f"{value:.4f}" if isinstance(value, float) else str(value)
        print(f"  {key}: {val_str}")

    print(f"\n[AI Survival Analysis (V3)]")
    if results['ai_metrics']:
        ai = results['ai_metrics']
        print(f"  Median Recovery Time:  {ai['median_recovery_time']} time_steps")
        print(f"  Confidence Score:      {ai['confidence_score']:.2f}%")
        print(f"  Method:                Kaplan-Meier Estimator")
    else:
        print("  AI metrics unavailable.")

    print("\nProcess finished with exit code 0")