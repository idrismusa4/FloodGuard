import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import { apiService, formatSeverity } from '../services/api';
import './FloodMap.css';

// Fix for default markers in react-leaflet
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const FloodMap = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Nigerian region coordinates
  const regionCoordinates = {
    'Abuja': [9.0765, 7.3986],
    'Lagos': [6.5244, 3.3792],
    'Kano': [12.0022, 8.5920],
    'Port Harcourt': [4.8156, 7.0498],
    'Ibadan': [7.3776, 3.9470],
    'Kaduna': [10.5200, 7.4382],
    'Benin City': [6.3350, 5.6037],
    'Jos': [9.9285, 8.8921],
    'Maiduguri': [11.8333, 13.1500],
    'Sokoto': [13.0059, 5.2476],
    'Ilorin': [8.5000, 4.5500],
    'Enugu': [6.4413, 7.4988],
    'Abeokuta': [7.1557, 3.3451],
    'Owerri': [5.4833, 7.0333],
    'Calabar': [4.9515, 8.3223]
  };

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAllRecentPredictions(50);
      setPredictions(response.data.predictions || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch predictions:', err);
      setError('Failed to load flood predictions');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    if (severity >= 0.7) return '#ef4444'; // Red - High risk
    if (severity >= 0.4) return '#f59e0b'; // Orange - Medium risk
    return '#10b981'; // Green - Low risk
  };

  const getSeverityRadius = (severity) => {
    // Scale radius based on severity (20-100 pixels)
    return Math.max(20, severity * 100);
  };

  const getLatestPrediction = (region) => {
    return predictions.find(p => p.region === region);
  };

  if (loading) {
    return (
      <div className="flood-map-container">
        <div className="map-loading">
          <p>Loading flood predictions...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flood-map-container">
        <div className="map-error">
          <p>{error}</p>
          <button onClick={fetchPredictions} className="retry-btn">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flood-map-container">
      <div className="map-header">
        <h2>Flood Risk Map - Nigeria</h2>
        <p>Real-time flood predictions across Nigerian regions</p>
        <div className="map-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#10b981' }}></div>
            <span>Low Risk (0-0.4)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#f59e0b' }}></div>
            <span>Medium Risk (0.4-0.7)</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#ef4444' }}></div>
            <span>High Risk (0.7-1.0)</span>
          </div>
        </div>
      </div>

      <div className="map-wrapper">
        <MapContainer
          center={[9.0765, 7.3986]} // Center on Nigeria
          zoom={6}
          style={{ height: '500px', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {Object.entries(regionCoordinates).map(([region, [lat, lng]]) => {
            const prediction = getLatestPrediction(region);
            const severity = prediction?.severity || 0;
            const color = getSeverityColor(severity);
            const radius = getSeverityRadius(severity);
            const riskLevel = formatSeverity(severity).level;

            return (
              <div key={region}>
                {/* Risk circle */}
                <Circle
                  center={[lat, lng]}
                  radius={radius * 1000} // Convert to meters
                  pathOptions={{
                    color: color,
                    fillColor: color,
                    fillOpacity: 0.3,
                    weight: 2
                  }}
                />
                
                {/* Region marker */}
                <Marker position={[lat, lng]}>
                  <Popup>
                    <div className="map-popup">
                      <h3>{region}</h3>
                      {prediction ? (
                        <>
                          <p><strong>Risk Level:</strong> <span style={{ color }}>{riskLevel}</span></p>
                          <p><strong>Severity:</strong> {(severity * 100).toFixed(1)}%</p>
                          <p><strong>Precipitation:</strong> {prediction.prediction_data?.precipitation_mm?.toFixed(1) || 'N/A'} mm</p>
                          <p><strong>Water Level:</strong> {prediction.prediction_data?.water_level_m?.toFixed(1) || 'N/A'} m</p>
                          <p><strong>Affected Population:</strong> {prediction.prediction_data?.affected_population?.toLocaleString() || 'N/A'}</p>
                          <p><strong>Last Updated:</strong> {new Date(prediction.created_at).toLocaleString()}</p>
                        </>
                      ) : (
                        <p>No recent prediction data</p>
                      )}
                    </div>
                  </Popup>
                </Marker>
              </div>
            );
          })}
        </MapContainer>
      </div>

      <div className="map-controls">
        <button onClick={fetchPredictions} className="refresh-btn">
          🔄 Refresh Predictions
        </button>
        <div className="map-stats">
          <span>Total Regions: {Object.keys(regionCoordinates).length}</span>
          <span>High Risk: {predictions.filter(p => p.severity >= 0.7).length}</span>
          <span>Medium Risk: {predictions.filter(p => p.severity >= 0.4 && p.severity < 0.7).length}</span>
          <span>Low Risk: {predictions.filter(p => p.severity < 0.4).length}</span>
        </div>
      </div>
    </div>
  );
};

export default FloodMap;
