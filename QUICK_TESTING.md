# ⚡ Quick Testing - Verification in 2 Minutes

## Fastest Method: Automatic Script

```powershell
python verify_setup.py
```

This script automatically checks all components and tells you exactly what's missing.

## Quick Manual Testing (3 steps)

### 1. Test Data Processing (30 seconds)

```powershell
cd data_processing
python satellite_data_processor_v2.py
```

**You should see:**
- "Processing flood event from..."
- "Processing complete!"
- "Recovery metrics: ..."

**If you see "ModuleNotFoundError" errors:**
```powershell
pip install -r requirements.txt
```

### 2. Test Backend (30 seconds)

In a new terminal:

```powershell
cd backend
python app.py
```

**You should see:**
```
Starting Post-Flood Recovery Analysis API...
API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!**

Then, in another terminal, test:

```powershell
curl http://localhost:5000/api/health
```

Should return: `{"status": "healthy", ...}`

### 3. Test Frontend (1 minute)

In a new terminal (backend must be running):

```powershell
cd frontend
npm start
```

**You should see:**
- Browser automatically opens at `http://localhost:3000`
- "Healing Map Dashboard" visible
- "Process Flood Event" form

**If you see errors:**
```powershell
npm install
```

## ✅ Final Verification (30 seconds)

In browser, at `http://localhost:3000`:

1. Fill the form:
   - Flood Date: `2023-06-15`
   - Latitude: `45.0`
   - Longitude: `25.0`
   - Number of Time Steps: `10`

2. Click "Process Flood Event"

3. You should see:
   - ✅ Success message
   - ✅ Event on map
   - ✅ Recovery metrics

## 🎯 If Everything Works

Congratulations! The project is functional. You can continue with:
- Processing more events
- Exploring the code
- Customizing the dashboard

## ❌ If Something Doesn't Work

1. Run `python verify_setup.py` for detailed diagnostics
2. Check `VERIFICATION.md` (Verification Guide) for solutions to common problems
3. Make sure all dependencies are installed

---

**Tip:** In PowerShell, use `;` instead of `&&` to run multiple commands.

