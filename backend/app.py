"""
Backend API for AI-Driven Satellite Platform
Post-Flood Landscape Recovery Analysis

This Flask API provides endpoints for:
- Data processing requests
- Recovery metrics retrieval
- Model inference
- Dashboard data serving
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime
import json

# Add parent directory to path to import data processing module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#importing V3
try:
    # Try importing V3
    from data_processing.satellite_data_processor_v3 import SatelliteAIProcessor
    print("✅ Loaded V3 AI Processor")
    ProcessorClass = SatelliteAIProcessor
except ImportError as e:
    # Print the ACTUAL error to help debugging
    print(f"⚠️ V3 Processor failed to load. Reason: {e}")
    print("⚠️ Falling back to V2 Processor.")
    try:
        from data_processing.satellite_data_processor_v2 import SatelliteDataProcessor
        ProcessorClass = SatelliteDataProcessor
    except ImportError:
        print("❌ No Data Processor found.")
        ProcessorClass = None

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# In-memory storage for demonstration (use database in production)
processed_events = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Post-Flood Recovery Analysis API',
        'version': '1.0.0'
    }), 200


@app.route('/api/process-flood-event', methods=['POST'])
def process_flood_event():
    """
    Process a flood event and calculate recovery metrics.
    
    Expected JSON body:
    {
        "flood_date": "2023-06-15",
        "location": {"lat": 45.0, "lon": 25.0},
        "num_time_steps": 10
    }
    """
    if ProcessorClass is None:
        return jsonify({
            'error': 'Data processing module not available'
        }), 500
    
    try:
        data = request.get_json()
        
        # Parse flood date
        flood_date_str = data.get('flood_date', '2023-06-15')
        flood_date = datetime.strptime(flood_date_str, '%Y-%m-%d')
        
        # Get other parameters
        location = data.get('location', {'lat': 45.0, 'lon': 25.0})
        num_time_steps = data.get('num_time_steps', 10)
        
        # Process the flood event
        processor = ProcessorClass()  # <--- Added ()
        if hasattr(processor, 'process_flood_event_ai'):
            results = processor.process_flood_event_ai(flood_date, num_time_steps)
        else:
            results = processor.process_flood_event(flood_date, num_time_steps)
        
        # Store results
        '''event_id = f"event_{flood_date_str}_{location['lat']}_{location['lon']}"
        processed_events[event_id] = {
            'flood_date': flood_date_str,
            'location': location,
            'recovery_metrics': results['recovery_metrics'],
            'time_series': results['time_series'].to_dict('records'),
            'processed_at': datetime.now().isoformat()
        }
        '''
        # Check if we should call the AI method or the Standard method
        if hasattr(processor, 'process_flood_event_ai'):
            results = processor.process_flood_event_ai(flood_date, num_time_steps)
        else:
            results = processor.process_flood_event(flood_date, num_time_steps)

        event_id = f"event_{flood_date_str}_{location['lat']}_{location['lon']}"

        # Safely get AI metrics if they exist
        ai_metrics = results.get('ai_metrics', None)

        processed_events[event_id] = {
            'flood_date': flood_date_str,
            'location': location,
            'recovery_metrics': results['recovery_metrics'],
            'ai_metrics': ai_metrics,
            'time_series': results['time_series'].to_dict('records'),
            'processed_at': datetime.now().isoformat()
        }
        return jsonify({
            'event_id': event_id,
            'status': 'processed',
            'recovery_metrics': results['recovery_metrics'],
            'time_series_length': len(results['time_series'])
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/recovery-metrics/<event_id>', methods=['GET'])
def get_recovery_metrics(event_id):
    """Get recovery metrics for a specific event."""
    if event_id not in processed_events:
        return jsonify({
            'error': 'Event not found'
        }), 404
    
    event_data = processed_events[event_id]
    return jsonify({
        'event_id': event_id,
        'recovery_metrics': event_data['recovery_metrics'],
        'ai_metrics': event_data.get('ai_metrics'),
        'time_series': event_data['time_series']
    }), 200


@app.route('/api/events', methods=['GET'])
def list_events():
    """List all processed flood events."""
    events_list = []
    for event_id, event_data in processed_events.items():
        events_list.append({
            'event_id': event_id,
            'flood_date': event_data['flood_date'],
            'location': event_data['location'],
            'recovery_percentage': event_data['recovery_metrics'].get('recovery_percentage', 0),
            'processed_at': event_data['processed_at']
        })
    
    return jsonify({
        'events': events_list,
        'count': len(events_list)
    }), 200


@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """
    Get aggregated data for the Healing Map Dashboard.
    """
    # Aggregate data from all events
    dashboard_data = {
        'total_events': len(processed_events),
        'events': []
    }
    
    for event_id, event_data in processed_events.items():
        dashboard_data['events'].append({
            'id': event_id,
            'flood_date': event_data['flood_date'],
            'location': event_data['location'],
            'recovery_percentage': event_data['recovery_metrics'].get('recovery_percentage', 0),
            'recovery_rate': event_data['recovery_metrics'].get('recovery_rate', 0),
            'time_to_recovery_days': event_data['recovery_metrics'].get('time_to_recovery_days'),
            'current_ndvi': event_data['recovery_metrics'].get('current_ndvi', 0)
        })
    
    return jsonify(dashboard_data), 200


@app.route('/api/survival-analysis/predict', methods=['POST'])
def predict_recovery():
    """
    Predict recovery probability using survival analysis.
    
    Expected JSON body:
    {
        "ndvi_current": 0.4,
        "ndwi_current": 0.2,
        "vv_backscatter": -15.0,
        "days_since_flood": 30
    }
    """
    try:
        data = request.get_json()
        
        # Simplified survival analysis prediction
        # In production, this would use the actual lifelines library
        ndvi_current = data.get('ndvi_current', 0.4)
        days_since_flood = data.get('days_since_flood', 30)
        
        # Simple heuristic model (replace with actual survival analysis)
        if ndvi_current < 0.3:
            recovery_probability_30d = 0.2
            recovery_probability_90d = 0.6
            recovery_probability_180d = 0.85
        elif ndvi_current < 0.5:
            recovery_probability_30d = 0.4
            recovery_probability_90d = 0.75
            recovery_probability_180d = 0.95
        else:
            recovery_probability_30d = 0.7
            recovery_probability_90d = 0.9
            recovery_probability_180d = 0.98
        
        return jsonify({
            'recovery_probabilities': {
                '30_days': recovery_probability_30d,
                '90_days': recovery_probability_90d,
                '180_days': recovery_probability_180d
            },
            'predicted_recovery_days': int(90 * (1 - recovery_probability_90d) + 30 * recovery_probability_30d)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("Starting Post-Flood Recovery Analysis API...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

