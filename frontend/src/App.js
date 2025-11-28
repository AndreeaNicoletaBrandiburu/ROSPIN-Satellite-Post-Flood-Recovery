import React, { useState, useEffect } from 'react';
import './App.css';
import HealingMap from './components/HealingMap';
import RecoveryMetrics from './components/RecoveryMetrics';
import EventProcessor from './components/EventProcessor';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/dashboard-data`);
      setEvents(response.data.events || []);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEventProcessed = () => {
    fetchEvents();
  };

  const handleEventSelect = (event) => {
    setSelectedEvent(event);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Driven Satellite Platform</h1>
        <h2>Post-Flood Landscape Recovery Analysis</h2>
        <p className="subtitle">Healing Map Dashboard</p>
      </header>

      <main className="App-main">
        <div className="dashboard-container">
          <div className="left-panel">
            <EventProcessor onEventProcessed={handleEventProcessed} />
            <RecoveryMetrics 
              events={events} 
              selectedEvent={selectedEvent}
              onEventSelect={handleEventSelect}
            />
          </div>
          
          <div className="right-panel">
            <HealingMap 
              events={events}
              selectedEvent={selectedEvent}
              onEventSelect={handleEventSelect}
            />
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>ROSPIN Project - Satellite Post-Flood Recovery Analysis</p>
      </footer>
    </div>
  );
}

export default App;

