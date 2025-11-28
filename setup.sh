#!/bin/bash

# Setup script for ROSPIN Satellite Post-Flood Recovery Project

echo "Setting up ROSPIN Satellite Post-Flood Recovery Project..."
echo ""

# Setup data processing
echo "Setting up data processing module..."
cd data_processing
pip install -r requirements.txt
cd ..

# Setup backend
echo "Setting up backend API..."
cd backend
pip install -r requirements.txt
cd ..

# Setup frontend
echo "Setting up frontend dashboard..."
cd frontend
npm install
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "1. Start backend: cd backend && python app.py"
echo "2. Start frontend: cd frontend && npm start"
echo "3. Open http://localhost:3000 in your browser"

