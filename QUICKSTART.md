# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

**Windows (PowerShell):**
```powershell
.\setup.bat
```

Sau manual în PowerShell:
```powershell
cd data_processing; pip install -r requirements.txt
cd ..\backend; pip install -r requirements.txt
cd ..\frontend; npm install
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual Installation (PowerShell):**

1. **Data Processing:**
   ```powershell
   cd data_processing
   pip install -r requirements.txt
   ```

2. **Backend:**
   ```powershell
   cd ..\backend
   pip install -r requirements.txt
   ```

3. **Frontend:**
   ```powershell
   cd ..\frontend
   npm install
   ```

**Notă:** În PowerShell, folosește `;` pentru a rula mai multe comenzi pe aceeași linie, sau rulează-le separat.

### Step 2: Start the Backend

Open a terminal and run:
```bash
cd backend
python app.py
```

You should see:
```
Starting Post-Flood Recovery Analysis API...
API will be available at http://localhost:5000
```

### Step 3: Start the Frontend

Open a **new terminal** and run:
```bash
cd frontend
npm start
```

The dashboard will automatically open in your browser at `http://localhost:3000`

### Step 4: Process Your First Flood Event

1. In the dashboard, use the **"Process Flood Event"** form
2. Enter:
   - Flood Date: Any date (e.g., 2023-06-15)
   - Latitude: 45.0
   - Longitude: 25.0
   - Number of Time Steps: 10
3. Click **"Process Flood Event"**
4. View the results on the Healing Map and Recovery Metrics panels

## 📊 Testing the Data Processing Module

Run the example:
```bash
cd data_processing
python example_usage.py
```

Or run the main processor:
```bash
python satellite_data_processor_v2.py
```

## 🔍 Verify Everything Works

1. **Backend Health Check:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Frontend:**
   - Open `http://localhost:3000`
   - You should see the "Healing Map Dashboard"

3. **Process an Event via API:**
   ```bash
   curl -X POST http://localhost:5000/api/process-flood-event \
     -H "Content-Type: application/json" \
     -d '{"flood_date": "2023-06-15", "location": {"lat": 45.0, "lon": 25.0}, "num_time_steps": 10}'
   ```

## 🐛 Troubleshooting

### Backend won't start
- Make sure port 5000 is not in use
- Check Python version: `python --version` (should be 3.8+)
- Verify dependencies: `pip list | grep flask`

### Frontend won't start
- Make sure port 3000 is not in use
- Check Node version: `node --version` (should be 16+)
- Try deleting `node_modules` and running `npm install` again

### API connection errors
- Make sure backend is running on port 5000
- Check `frontend/.env` has correct `REACT_APP_API_URL`

## 📚 Next Steps

- Read the main [README.md](README.md) for detailed documentation
- Explore the code in `data_processing/satellite_data_processor_v2.py`
- Check API endpoints in `backend/app.py`
- Customize the dashboard in `frontend/src/`

---

**Need Help?** Check the main README.md for comprehensive documentation.

