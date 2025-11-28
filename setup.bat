@echo off
REM Setup script for ROSPIN Satellite Post-Flood Recovery Project (Windows)

echo Setting up ROSPIN Satellite Post-Flood Recovery Project...
echo.

REM Setup data processing
echo Setting up data processing module...
cd data_processing
pip install -r requirements.txt
cd ..

REM Setup backend
echo Setting up backend API...
cd backend
pip install -r requirements.txt
cd ..

REM Setup frontend
echo Setting up frontend dashboard...
cd frontend
call npm install
cd ..

echo.
echo Setup complete!
echo.
echo To run the application:
echo.
echo In PowerShell, use semicolon (;) instead of &&:
echo   1. Start backend: cd backend; python app.py
echo   2. Start frontend (new terminal): cd frontend; npm start
echo.
echo Or run commands separately:
echo   1. cd backend
echo      python app.py
echo   2. cd frontend (in new terminal)
echo      npm start
echo.
echo 3. Open http://localhost:3000 in your browser

pause

