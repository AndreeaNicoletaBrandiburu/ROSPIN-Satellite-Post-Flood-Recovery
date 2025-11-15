# Satellite Data Processing Module V1 (ROSPIN HW3)

This repository contains the deliverable for the HW3 assignment. It includes the first iteration of a satellite data processing module, as part of the "AI-Driven Satellite Platform for Post-Flood Landscape Recovery Analysis" project.

## 🎯 Project Goal (HW3)

The requirement for this iteration was to create a script demonstrating:
1.  **Basic Data Loading**
2.  **Simple Computations**

## Implementation

This module is a Google Colab notebook (`satellite_data_processor_v1.ipynb`) that fulfills the requirements by:

* **Loading:** Simulating the loading of **Sentinel-2 Band 4 (Red)** and **Band 8 (NIR)** data using `numpy`.
* **Computation:** Performing a simple and relevant computation: calculating the **Normalized Difference Vegetation Index (NDVI)**, a key metric for monitoring vegetation health and recovery.

## 🚀 How to Run

1.  **Open in Google Colab:**
    * [**Click here to open the notebook directly in Colab**](https://colab.research.google.com/github/AndreeaNicoletaBrandiburu/ROSPIN-Satellite-Post-Flood-Recovery/blob/main/satellite_data_processor_v1.ipynb)

2.  **Run the Cells:**
    * In the Colab interface, select `Runtime` > `Run all` from the top menu.

3.  **Observe the Output:**
    * The script will first install the `rasterio` dependency.
    * It will then execute the main script, printing the status of the data loading and computation steps.
    * Finally, it will display a simulated NDVI map as the output.

---