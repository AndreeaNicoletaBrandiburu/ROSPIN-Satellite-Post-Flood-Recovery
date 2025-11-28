import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './HealingMap.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const HealingMap = ({ events, selectedEvent, onEventSelect }) => {
  const defaultCenter = [45.0, 25.0]; // Default to Romania
  const defaultZoom = 6;

  const getRecoveryColor = (recoveryPercentage) => {
    if (recoveryPercentage >= 80) return '#51cf66'; // Green - recovered
    if (recoveryPercentage >= 50) return '#ffd43b'; // Yellow - recovering
    if (recoveryPercentage >= 20) return '#ff922b'; // Orange - slow recovery
    return '#ff6b6b'; // Red - minimal recovery
  };

  const getRecoveryRadius = (recoveryPercentage) => {
    // Scale radius based on recovery (min 5000m, max 20000m)
    return 5000 + (recoveryPercentage / 100) * 15000;
  };

  return (
    <div className="card healing-map-container">
      <h3>Healing Map - Recovery Status</h3>
      <div className="map-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#51cf66' }}></span>
          <span>Recovered (80-100%)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ffd43b' }}></span>
          <span>Recovering (50-79%)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ff922b' }}></span>
          <span>Slow Recovery (20-49%)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ff6b6b' }}></span>
          <span>Minimal Recovery (0-19%)</span>
        </div>
      </div>
      
      <MapContainer
        center={selectedEvent ? [selectedEvent.location.lat, selectedEvent.location.lon] : defaultCenter}
        zoom={selectedEvent ? 10 : defaultZoom}
        style={{ height: '600px', width: '100%', borderRadius: '8px' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {events.map((event) => {
          const color = getRecoveryColor(event.recovery_percentage);
          const radius = getRecoveryRadius(event.recovery_percentage);
          const isSelected = selectedEvent && selectedEvent.id === event.id;
          
          return (
            <React.Fragment key={event.id}>
              <Circle
                center={[event.location.lat, event.location.lon]}
                radius={radius}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.3,
                  weight: isSelected ? 3 : 2
                }}
                eventHandlers={{
                  click: () => onEventSelect(event)
                }}
              />
              <Marker
                position={[event.location.lat, event.location.lon]}
                eventHandlers={{
                  click: () => onEventSelect(event)
                }}
              >
                <Popup>
                  <div className="map-popup">
                    <h4>Flood Event</h4>
                    <p><strong>Date:</strong> {event.flood_date}</p>
                    <p><strong>Recovery:</strong> {event.recovery_percentage.toFixed(1)}%</p>
                    <p><strong>Recovery Rate:</strong> {event.recovery_rate?.toFixed(4) || 'N/A'}</p>
                    {event.time_to_recovery_days && (
                      <p><strong>Est. Recovery Time:</strong> {Math.round(event.time_to_recovery_days)} days</p>
                    )}
                  </div>
                </Popup>
              </Marker>
            </React.Fragment>
          );
        })}
      </MapContainer>
      
      {events.length === 0 && (
        <div className="no-events-message">
          <p>No flood events processed yet. Use the Event Processor to add events.</p>
        </div>
      )}
    </div>
  );
};

export default HealingMap;

