import React, { useState, useEffect } from 'react';
import { apiService, formatSeverity } from '../services/api';
import FloodMap from './FloodMap';
import './PredictionMap.css';

const PredictionMap = () => {
  const [selectedRegion, setSelectedRegion] = useState('Abuja');
  const [prediction, setPrediction] = useState(null);
  const [allPredictions, setAllPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const nigerianRegions = [
    'Abuja', 'Lagos', 'Kano', 'Port Harcourt', 'Ibadan', 
    'Kaduna', 'Benin City', 'Jos', 'Maiduguri', 'Sokoto',
    'Ilorin', 'Enugu', 'Abeokuta', 'Owerri', 'Calabar'
  ];

  useEffect(() => {
    fetchAllPredictions();
  }, []);

  useEffect(() => {
    if (selectedRegion) {
      fetchRegionPrediction(selectedRegion);
    }
  }, [selectedRegion]);

  const fetchAllPredictions = async () => {
    try {
      const response = await apiService.getAllRecentPredictions(50);
      setAllPredictions(response.data.predictions || []);
    } catch (err) {
      console.error('Failed to fetch all predictions:', err);
    }
  };

  const fetchRegionPrediction = async (region) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getPrediction(region);
      setPrediction(response.data.prediction);
    } catch (err) {
      console.error('Failed to fetch prediction:', err);
      setError(`Failed to get prediction for ${region}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRegionSelect = (region) => {
    setSelectedRegion(region);
  };

  const generateNewPrediction = async () => {
    if (!selectedRegion) return;
    await fetchRegionPrediction(selectedRegion);
    await fetchAllPredictions();
  };

  const getSeverityColor = (severity) => {
    if (severity >= 0.7) return '#ef4444';
    if (severity >= 0.4) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="prediction-map">
      <div className="prediction-header">
        <h1>Flood Predictions</h1>
        <p>Real-time flood risk assessment powered by NVIDIA Earth-2</p>
      </div>

      <div className="grid grid-cols-3">
        {/* Region Selector */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Select Region</h2>
          </div>
          
          <div className="region-list">
            {nigerianRegions.map((region) => (
              <button
                key={region}
                className={`region-button ${selectedRegion === region ? 'active' : ''}`}
                onClick={() => handleRegionSelect(region)}
              >
                <span className="region-name">{region}</span>
                {allPredictions.find(p => p.region === region) && (
                  <span 
                    className="region-status"
                    style={{ 
                      backgroundColor: getSeverityColor(
                        allPredictions.find(p => p.region === region)?.severity || 0
                      )
                    }}
                  ></span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Prediction Details */}
        <div className="card prediction-details">
          <div className="card-header">
            <h2 className="card-title">
              Prediction for {selectedRegion}
            </h2>
            <button 
              className="btn btn-primary"
              onClick={generateNewPrediction}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>

          {error && (
            <div className="error">
              <p>{error}</p>
            </div>
          )}

          {loading && !prediction && (
            <div className="loading">
              <p>Getting prediction from Earth-2...</p>
            </div>
          )}

          {prediction && (
            <div className="prediction-content">
              <div className="severity-display">
                <div 
                  className="severity-circle"
                  style={{ backgroundColor: getSeverityColor(prediction.severity) }}
                >
                  {(prediction.severity * 100).toFixed(0)}%
                </div>
                <div className="severity-info">
                  <h3>Risk Level: {formatSeverity(prediction.severity).level}</h3>
                  <p>Confidence: {((prediction.confidence || 0.8) * 100).toFixed(0)}%</p>
                </div>
              </div>

              <div className="prediction-metrics">
                <div className="metric">
                  <label>Precipitation</label>
                  <value>{prediction.precipitation_mm?.toFixed(1) || 'N/A'} mm</value>
                </div>
                
                <div className="metric">
                  <label>Water Level</label>
                  <value>{prediction.water_level_m?.toFixed(1) || 'N/A'} m</value>
                </div>
                
                <div className="metric">
                  <label>Affected Population</label>
                  <value>{prediction.affected_population?.toLocaleString() || 'N/A'}</value>
                </div>
                
                <div className="metric">
                  <label>Forecast Period</label>
                  <value>{prediction.forecast_hours || 72} hours</value>
                </div>
              </div>

              <div className="prediction-timestamp">
                <p>Last updated: {new Date(prediction.timestamp || Date.now()).toLocaleString()}</p>
              </div>
            </div>
          )}
        </div>

        {/* Interactive Flood Map */}
        <div className="card map-card">
          <div className="card-header">
            <h2 className="card-title">Interactive Risk Map</h2>
          </div>
          
          <FloodMap />
        </div>
      </div>

      {/* Recent Predictions Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Predictions</h2>
        </div>
        
        <div className="predictions-table">
          <div className="table-header">
            <span>Region</span>
            <span>Severity</span>
            <span>Risk Level</span>
            <span>Population</span>
            <span>Timestamp</span>
          </div>
          
          {allPredictions.slice(0, 10).map((pred) => {
            const severity = formatSeverity(pred.severity);
            return (
              <div key={pred.id} className="table-row">
                <span className="region-cell">{pred.region}</span>
                <span className="severity-cell">
                  <div 
                    className="severity-bar"
                    style={{ 
                      width: `${pred.severity * 100}%`,
                      backgroundColor: getSeverityColor(pred.severity)
                    }}
                  ></div>
                  {(pred.severity * 100).toFixed(0)}%
                </span>
                <span className={`risk-cell ${severity.color}`}>
                  {severity.level}
                </span>
                <span className="population-cell">
                  {pred.prediction_data?.affected_population?.toLocaleString() || 'N/A'}
                </span>
                <span className="time-cell">
                  {new Date(pred.created_at).toLocaleString()}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default PredictionMap;

