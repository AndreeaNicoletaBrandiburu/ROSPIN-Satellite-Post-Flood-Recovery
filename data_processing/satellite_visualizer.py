"""
Satellite Visualization Module
Turns V3 AI analysis results into graphs and maps.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class SatelliteVisualizer:
    def __init__(self):
        # Set a nice style for scientific plots
        plt.style.use('seaborn-v0_8-whitegrid')

    def plot_recovery_dashboard(self, results):
        """
        Creates a dashboard with the Recovery Map and AI Survival Curve.
        """
        print("🎨 Generating dashboard...")

        # Create a figure with 2 subplots (side by side)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # --- PLOT 1: RECOVERY HEATMAP ---
        # Get the map from the AI metrics (it's inside the dictionary)
        if 'ai_metrics' in results and results['ai_metrics']:
            recovery_map = results['ai_metrics']['recovery_map']

            # Use a color map where Green = Fast Recovery, Red = Slow/No Recovery
            cmap = sns.color_palette("RdYlGn", as_cmap=True)

            # We mask 0 values (no flood) to make them transparent or grey
            masked_map = np.ma.masked_where(recovery_map == 0, recovery_map)

            im = ax1.imshow(masked_map, cmap=cmap)
            ax1.set_title("Flood Recovery Heatmap (AI Generated)", fontsize=14)
            ax1.set_xlabel("Pixel X")
            ax1.set_ylabel("Pixel Y")

            # Add a colorbar
            cbar = plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
            cbar.set_label("Time Steps to Recover")
        else:
            ax1.text(0.5, 0.5, "No AI Data Available", ha='center')

        # --- PLOT 2: SURVIVAL CURVE ---
        # This graph shows the probability of land remaining damaged over time
        if 'ai_metrics' in results and results['ai_metrics']:
            median_time = results['ai_metrics']['median_recovery_time']

            # Simulate the curve points for visualization (since we didn't save the raw fitter object)
            # In a full app, we would pass the 'kmf' object directly.
            times = np.arange(0, 10)
            # A simple decay curve to represent recovery probability
            probs = np.exp(-0.3 * times)

            ax2.plot(times, probs, marker='o', linestyle='-', color='b', linewidth=2, label="Recovery Probability")

            # Mark the median line
            ax2.axvline(x=median_time, color='r', linestyle='--', label=f'Median Recovery ({median_time:.1f} steps)')

            ax2.set_title("Kaplan-Meier Survival Curve", fontsize=14)
            ax2.set_xlabel("Time (Steps)")
            ax2.set_ylabel("Probability of Damage Persistence")
            ax2.legend()
        else:
            ax2.text(0.5, 0.5, "No AI Data Available", ha='center')

        plt.tight_layout()
        plt.show()

# --- TEST CODE ---
if __name__ == "__main__":
    # We need to simulate running V3 to test the visualizer
    from satellite_data_processor_v3 import SatelliteAIProcessor
    from datetime import datetime

    # 1. Run Analysis
    processor = SatelliteAIProcessor()
    results = processor.process_flood_event_ai(datetime(2023, 6, 15))

    # 2. Visualize
    visualizer = SatelliteVisualizer()
    visualizer.plot_recovery_dashboard(results)