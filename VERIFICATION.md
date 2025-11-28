# 🔍 Verification Guide - How to Verify the Project Works

## Method 1: Automatic Verification Script

Run the verification script:

```powershell
python verify_setup.py
```

This script will verify:
- ✅ Python version
- ✅ Python packages installed
- ✅ Node.js installed
- ✅ npm packages installed
- ✅ Data processing module
- ✅ Backend API
- ✅ File structure

## Method 2: Manual Step-by-Step Verification

### Step 1: Check Python

```powershell
python --version
```

Should be Python 3.8 or newer.

### Step 2: Install Python Dependencies

**IMPORTANT:** In PowerShell, use `;` instead of `&&`:

```powershell
cd data_processing; pip install -r requirements.txt
cd ..\backend; pip install -r requirements.txt
```

Or separate commands:

```powershell
cd data_processing
pip install -r requirements.txt
cd ..\backend
pip install -r requirements.txt
```

### Step 3: Test Data Processing Module

```powershell
cd data_processing
python satellite_data_processor_v2.py
```

You should see output with:
- "Processing flood event from..."
- "Processing complete!"
- "Recovery metrics: ..."

### Step 4: Check Node.js

```powershell
node --version
npm --version
```

### Step 5: Install Frontend Dependencies

```powershell
cd frontend
npm install
```

Wait until installation completes (may take a few minutes).

### Step 6: Test Backend API

In a PowerShell terminal:

```powershell
cd backend
python app.py
```

You should see:
```
Starting Post-Flood Recovery Analysis API...
API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!**

### Step 7: Test Frontend

Open a **NEW PowerShell terminal** (keep backend running):

```powershell
cd frontend
npm start
```

Browser should automatically open at `http://localhost:3000`

### Step 8: Test Complete Functionality

1. **In browser** (at `http://localhost:3000`):
   - You should see "Healing Map Dashboard"
   - "Process Flood Event" form

2. **Fill the form:**
   - Flood Date: `2023-06-15`
   - Latitude: `45.0`
   - Longitude: `25.0`
   - Number of Time Steps: `10`
   - Click "Process Flood Event"

3. **Check results:**
   - You should see a success message
   - Event should appear on the map
   - Click on event to see metrics

## Method 3: Quick API Testing

If backend is running, test the API directly:

```powershell
# Test health check
curl http://localhost:5000/api/health

# Test event processing
curl -X POST http://localhost:5000/api/process-flood-event -H "Content-Type: application/json" -d '{\"flood_date\": \"2023-06-15\", \"location\": {\"lat\": 45.0, \"lon\": 25.0}, \"num_time_steps\": 10}'
```

## ⚠️ Common Issues and Solutions

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies:
```powershell
pip install -r data_processing/requirements.txt
pip install -r backend/requirements.txt
```

### Issue: "node: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: Port 5000 or 3000 already in use
**Solution:** 
- Close other applications using these ports
- Or change ports in configuration

### Issue: Frontend doesn't connect to backend
**Solution:**
- Verify backend is running on port 5000
- Check browser console for errors (F12)
- Verify `frontend/package.json` has `"proxy": "http://localhost:5000"`

## ✅ Final Checklist

- [ ] Python 3.8+ installed
- [ ] All Python packages installed
- [ ] Node.js installed
- [ ] npm packages installed
- [ ] Data processing module works
- [ ] Backend API starts without errors
- [ ] Frontend starts without errors
- [ ] Dashboard opens in browser
- [ ] Can process a flood event
- [ ] Results appear on map

## 📞 If You Have Issues

1. Run `python verify_setup.py` for automatic diagnostics
2. Check error messages in terminal
3. Verify all ports are free
4. Make sure all dependencies are installed

---

**Note:** In PowerShell, use `;` to run multiple commands on the same line, or run them separately.

