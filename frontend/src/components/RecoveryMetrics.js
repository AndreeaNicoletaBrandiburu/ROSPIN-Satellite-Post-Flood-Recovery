import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './RecoveryMetrics.css';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const RecoveryMetrics = ({ events, selectedEvent, onEventSelect }) => {
  const [timeSeriesData, setTimeSeriesData] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    if (selectedEvent) {
      fetchTimeSeries(selectedEvent.id);
    }
  }, [selectedEvent]);

  const fetchTimeSeries = async (eventId) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/recovery-metrics/${eventId}`);
      if (response.data.time_series) {
        setTimeSeriesData(response.data.time_series);
      }
    } catch (error) {
      console.error('Error fetching time series:', error);
      setTimeSeriesData([]);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const chartData = timeSeriesData.map(item => ({
    date: formatDate(item.date),
    NDVI: item.mean_ndvi ? (item.mean_ndvi * 100).toFixed(1) : null,
    NDWI: item.mean_ndwi ? (item.mean_ndwi * 100).toFixed(1) : null
  }));

  return (
    <div className="card recovery-metrics-container">
      <h3>Recovery Metrics</h3>
      
      {selectedEvent ? (
        <>
          <div className="metrics-summary">
            <div className="metric-item">
              <span className="metric-label">Recovery Percentage</span>
              <span className="metric-value">{selectedEvent.recovery_percentage.toFixed(1)}%</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Recovery Rate</span>
              <span className="metric-value">{selectedEvent.recovery_rate?.toFixed(4) || 'N/A'}</span>
            </div>
            {selectedEvent.time_to_recovery_days && (
              <div className="metric-item">
                <span className="metric-label">Est. Recovery Time</span>
                <span className="metric-value">{Math.round(selectedEvent.time_to_recovery_days)} days</span>
              </div>
            )}
            <div className="metric-item">
              <span className="metric-label">Current NDVI</span>
              <span className="metric-value">{selectedEvent.current_ndvi?.toFixed(3) || 'N/A'}</span>
            </div>
          </div>

          {loading ? (
            <div className="loading">Loading time series data...</div>
          ) : chartData.length > 0 ? (
            <div className="chart-container">
              <h4>Time Series Analysis</h4>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                  <XAxis dataKey="date" stroke="#a0d0ff" />
                  <YAxis stroke="#a0d0ff" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(20, 30, 50, 0.95)', 
                      border: '1px solid rgba(100, 200, 255, 0.3)',
                      color: '#ffffff'
                    }} 
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="NDVI" 
                    stroke="#51cf66" 
                    strokeWidth={2}
                    dot={{ fill: '#51cf66' }}
                    name="NDVI (%)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="NDWI" 
                    stroke="#4a9eff" 
                    strokeWidth={2}
                    dot={{ fill: '#4a9eff' }}
                    name="NDWI (%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="no-data">No time series data available</div>
          )}
        </>
      ) : (
        <div className="no-selection">
          <p>Select an event from the map or list below to view recovery metrics.</p>
          
          {events.length > 0 && (
            <div className="events-list">
              <h4>Recent Events</h4>
              <ul>
                {events.map(event => (
                  <li 
                    key={event.id} 
                    className={selectedEvent?.id === event.id ? 'selected' : ''}
                    onClick={() => onEventSelect(event)}
                  >
                    <div className="event-item">
                      <span className="event-date">{event.flood_date}</span>
                      <span className="event-recovery">{event.recovery_percentage.toFixed(1)}%</span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RecoveryMetrics;

