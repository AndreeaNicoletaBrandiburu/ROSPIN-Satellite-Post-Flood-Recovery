import React, { useState } from 'react';
import axios from 'axios';
import './EventProcessor.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const EventProcessor = ({ onEventProcessed }) => {
  const [formData, setFormData] = useState({
    flood_date: new Date().toISOString().split('T')[0],
    lat: '45.0',
    lon: '25.0',
    num_time_steps: '10'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [messageType, setMessageType] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    setMessageType(null);

    try {
      const payload = {
        flood_date: formData.flood_date,
        location: {
          lat: parseFloat(formData.lat),
          lon: parseFloat(formData.lon)
        },
        num_time_steps: parseInt(formData.num_time_steps)
      };

      const response = await axios.post(`${API_BASE_URL}/process-flood-event`, payload);
      
      setMessage(`Event processed successfully! Event ID: ${response.data.event_id}`);
      setMessageType('success');
      
      // Reset form
      setFormData({
        flood_date: new Date().toISOString().split('T')[0],
        lat: '45.0',
        lon: '25.0',
        num_time_steps: '10'
      });

      // Notify parent component
      if (onEventProcessed) {
        onEventProcessed();
      }
    } catch (error) {
      setMessage(error.response?.data?.error || 'Error processing flood event. Please try again.');
      setMessageType('error');
      console.error('Error processing event:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card event-processor">
      <h3>Process Flood Event</h3>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="flood_date">Flood Date</label>
          <input
            type="date"
            id="flood_date"
            name="flood_date"
            value={formData.flood_date}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="input-row">
          <div className="input-group">
            <label htmlFor="lat">Latitude</label>
            <input
              type="number"
              id="lat"
              name="lat"
              value={formData.lat}
              onChange={handleInputChange}
              step="0.0001"
              min="-90"
              max="90"
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="lon">Longitude</label>
            <input
              type="number"
              id="lon"
              name="lon"
              value={formData.lon}
              onChange={handleInputChange}
              step="0.0001"
              min="-180"
              max="180"
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="num_time_steps">Number of Time Steps</label>
          <input
            type="number"
            id="num_time_steps"
            name="num_time_steps"
            value={formData.num_time_steps}
            onChange={handleInputChange}
            min="1"
            max="50"
            required
          />
          <small className="input-hint">Number of time periods to analyze (recommended: 8-12)</small>
        </div>

        {message && (
          <div className={messageType === 'error' ? 'error' : 'success'}>
            {message}
          </div>
        )}

        <button type="submit" className="button" disabled={loading}>
          {loading ? 'Processing...' : 'Process Flood Event'}
        </button>
      </form>
    </div>
  );
};

export default EventProcessor;

