# AI-Driven Satellite Platform for Post-Flood Landscape Recovery Analysis

This repository contains the full-stack application and data processing pipeline for the **AI-Driven Satellite Platform for Post-Flood Landscape Recovery Analysis** project, developed as part of the ROSPIN course assignments (HW4 and HW5).

## 🎯 Project Overview

This platform integrates **Sentinel-1 (Radar)** and **Sentinel-2 (Optical)** satellite data to track and analyze post-flood landscape recovery. The system calculates key metrics including:

- **NDVI (Normalized Difference Vegetation Index)** - Vegetation health monitoring
- **NDWI (Normalized Difference Water Index)** - Water content analysis
- **Radar Backscatter** - All-weather monitoring capability
- **Recovery Metrics** - Time-to-recovery analysis using survival analysis models

The platform provides an intuitive **Healing Map Dashboard** for stakeholders including governments, NGOs, agricultural bodies, and insurance companies.

## 📁 Project Structure

```
ROSPIN-Satellite-Post-Flood-Recovery/
│
├── data_processing/              # Data processing pipeline (V2)
│   ├── satellite_data_processor_v2.py
│   └── requirements.txt
│
├── backend/                      # Flask API backend
│   ├── app.py
│   └── requirements.txt
│
├── frontend/                     # React dashboard
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HealingMap.js
│   │   │   ├── RecoveryMetrics.js
│   │   │   └── EventProcessor.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and **npm**
- **Git**

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd ROSPIN-Satellite-Post-Flood-Recovery
```

#### 2. Set Up Data Processing Module

```bash
cd data_processing
pip install -r requirements.txt
```

#### 3. Set Up Backend API

```bash
cd ../backend
pip install -r requirements.txt
```

#### 4. Set Up Frontend Dashboard

```bash
cd ../frontend
npm install
```

## 🏃 Running the Application

### Start the Backend API

From the `backend` directory:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

**API Endpoints:**
- `GET /api/health` - Health check
- `POST /api/process-flood-event` - Process a new flood event
- `GET /api/recovery-metrics/<event_id>` - Get recovery metrics for an event
- `GET /api/events` - List all processed events
- `GET /api/dashboard-data` - Get aggregated dashboard data
- `POST /api/survival-analysis/predict` - Predict recovery using survival analysis

### Start the Frontend Dashboard

From the `frontend` directory:

```bash
npm start
```

The dashboard will open at `http://localhost:3000`

### Run Data Processing Module

From the `data_processing` directory:

```bash
python satellite_data_processor_v2.py
```

## 📊 Features

### Data Processing Pipeline (V2)

**Improvements over V1:**
- ✅ Multi-sensor data integration (Sentinel-1 + Sentinel-2)
- ✅ NDVI, NDWI, and radar backscatter calculations
- ✅ Time-series analysis
- ✅ Recovery metrics computation
- ✅ Support for multiple time steps

**Key Classes:**
- `SatelliteDataProcessor` - Main processing class
- Methods for loading, calculating indices, and analyzing recovery

### Full-Stack Application

**Backend (Flask API):**
- RESTful API for data processing
- Event management
- Recovery metrics calculation
- Survival analysis predictions

**Frontend (React Dashboard):**
- **Healing Map** - Interactive map showing recovery status
- **Recovery Metrics** - Time-series charts and statistics
- **Event Processor** - Interface to process new flood events
- Real-time data visualization

## 🔧 Configuration

### Backend Configuration

Create a `.env` file in the `backend` directory (optional):

```
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
```

### Frontend Configuration

The frontend is configured to connect to `http://localhost:5000` by default. To change this, create a `.env` file in the `frontend` directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## 📝 Usage Examples

### Processing a Flood Event via API

```bash
curl -X POST http://localhost:5000/api/process-flood-event \
  -H "Content-Type: application/json" \
  -d '{
    "flood_date": "2023-06-15",
    "location": {"lat": 45.0, "lon": 25.0},
    "num_time_steps": 10
  }'
```

### Using the Data Processing Module

```python
from data_processing.satellite_data_processor_v2 import SatelliteDataProcessor
from datetime import datetime

# Initialize processor
processor = SatelliteDataProcessor()

# Process a flood event
flood_date = datetime(2023, 6, 15)
results = processor.process_flood_event(flood_date, num_time_steps=10)

# Access results
print(f"Recovery percentage: {results['recovery_metrics']['recovery_percentage']}%")
print(f"Time to recovery: {results['recovery_metrics']['time_to_recovery_days']} days")
```

## 🧪 Testing

### Test Backend API

```bash
cd backend
python -m pytest  # If tests are added
```

### Test Data Processing

```bash
cd data_processing
python satellite_data_processor_v2.py
```

## 📚 Documentation

### Data Processing Module

The `SatelliteDataProcessor` class provides:

- **`load_sentinel2_data()`** - Load optical satellite data
- **`load_sentinel1_data()`** - Load radar satellite data
- **`calculate_ndvi()`** - Calculate NDVI index
- **`calculate_ndwi()`** - Calculate NDWI index
- **`calculate_radar_backscatter()`** - Process radar data
- **`process_time_series()`** - Analyze temporal data
- **`calculate_recovery_metrics()`** - Compute recovery statistics
- **`process_flood_event()`** - Main processing function

### API Documentation

See the inline documentation in `backend/app.py` for detailed endpoint descriptions.

## 🎓 Assignment Deliverables

### HW4 Deliverables ✅
- [x] First working version of full-stack application
- [x] Second iteration of data processing code
- [x] Clear folder structure
- [x] README.md documentation

### HW5 Deliverables ✅
- [x] Final version of satellite data processing code
- [x] Second iteration of full-stack application (refined UI, backend, integration)

## 🔬 Technical Details

### Data Sources
- **Sentinel-1**: C-band SAR (Synthetic Aperture Radar) - All-weather monitoring
- **Sentinel-2**: Multi-spectral optical imagery - Vegetation and water indices

### Key Metrics
- **NDVI**: `(NIR - Red) / (NIR + Red)` - Range: -1 to 1
- **NDWI**: `(Green - NIR) / (Green + NIR)` - Range: -1 to 1
- **Radar Backscatter**: VV and VH polarizations in dB scale

### Recovery Analysis
- Time-series analysis of NDVI/NDWI trends
- Recovery rate calculation (slope of recovery curve)
- Time-to-recovery estimation
- Survival analysis for recovery probability prediction

## 🤝 Contributing

This is a course project. For questions or issues, please contact the project maintainer.

## 📄 License

This project is developed for educational purposes as part of the ROSPIN course.

## 🙏 Acknowledgments

- Copernicus Programme for Sentinel satellite data
- European Space Agency (ESA)
- Open-source libraries: React, Flask, NumPy, Pandas, Leaflet

---

**Project Status**: ✅ HW4 & HW5 Complete

**Last Updated**: November 2025
