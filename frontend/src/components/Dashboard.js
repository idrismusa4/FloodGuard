import React, { useState, useEffect } from 'react';
import { apiService, formatSeverity, formatNumber } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [recentPredictions, setRecentPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsResponse, predictionsResponse] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getAllRecentPredictions(10)
      ]);
      
      setStats(statsResponse.data.stats);
      setRecentPredictions(predictionsResponse.data.predictions || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !stats) {
    return (
      <div className="dashboard">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">
          <h3>⚠️ Error</h3>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={fetchDashboardData}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>FloodGuardian AI Dashboard</h1>
        <p>Real-time flood monitoring and emergency response coordination</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-4">
        <div className="stat-card">
          <div className="stat-icon">🌊</div>
          <div className="stat-content">
            <h3>{formatNumber(stats?.total_predictions || 0)}</h3>
            <p>Total Predictions</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📱</div>
          <div className="stat-content">
            <h3>{formatNumber(stats?.total_alerts_sent || 0)}</h3>
            <p>Alerts Sent</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>{formatNumber(stats?.registered_users || 0)}</h3>
            <p>Registered Users</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🚨</div>
          <div className="stat-content">
            <h3>{stats?.high_severity_regions || 0}</h3>
            <p>High Risk Regions</p>
          </div>
        </div>
      </div>

      {/* Recent Predictions */}
      <div className="grid grid-cols-2">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Recent Predictions</h2>
            <button 
              className="btn btn-secondary"
              onClick={fetchDashboardData}
              disabled={loading}
            >
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
          
          <div className="predictions-list">
            {recentPredictions.length > 0 ? (
              recentPredictions.map((prediction) => {
                const severity = formatSeverity(prediction.severity);
                return (
                  <div key={prediction.id} className="prediction-item">
                    <div className="prediction-header">
                      <h4>{prediction.region}</h4>
                      <span className={`status-badge ${severity.color}`}>
                        {severity.level}
                      </span>
                    </div>
                    <div className="prediction-details">
                      <p>Severity: {prediction.severity.toFixed(2)}</p>
                      <p className="prediction-time">
                        {new Date(prediction.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                );
              })
            ) : (
              <p className="no-data">No recent predictions available</p>
            )}
          </div>
        </div>

        {/* System Status */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">System Status</h2>
          </div>
          
          <div className="system-status-grid">
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>API Server</span>
              <span className="status-text">Online</span>
            </div>
            
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>Database</span>
              <span className="status-text">Connected</span>
            </div>
            
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>Earth-2 API</span>
              <span className="status-text">Available</span>
            </div>
            
            <div className="status-item">
              <div className="status-indicator online"></div>
              <span>SMS Service</span>
              <span className="status-text">Ready</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Quick Actions</h2>
        </div>
        
        <div className="quick-actions">
          <button className="btn btn-primary">
            🌊 Run Prediction Check
          </button>
          <button className="btn btn-danger">
            🚨 Send Emergency Alert
          </button>
          <button className="btn btn-success">
            🚛 Allocate Resources
          </button>
          <button className="btn btn-secondary">
            📊 Generate Report
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

