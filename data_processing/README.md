# Data Processing Module V2

This module contains the second iteration of the satellite data processing pipeline for post-flood recovery analysis.

## Features

- Multi-sensor data loading (Sentinel-1 and Sentinel-2)
- NDVI and NDWI calculation
- Radar backscatter processing
- Time-series analysis
- Recovery metrics computation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from satellite_data_processor_v2 import SatelliteDataProcessor
from datetime import datetime

processor = SatelliteDataProcessor()
results = processor.process_flood_event(datetime(2023, 6, 15), num_time_steps=10)
```

## Improvements over V1

- Added Sentinel-1 radar data support
- Implemented NDWI calculation
- Added time-series processing
- Recovery metrics computation
- Multi-temporal analysis

