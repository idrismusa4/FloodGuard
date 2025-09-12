import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './Alerts.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sendingAlert, setSendingAlert] = useState(false);
  
  // Form state
  const [alertForm, setAlertForm] = useState({
    region: 'Abuja',
    message: '',
    severityThreshold: 0.7
  });

  const nigerianRegions = [
    'Abuja', 'Lagos', 'Kano', 'Port Harcourt', 'Ibadan', 
    'Kaduna', 'Benin City', 'Jos', 'Maiduguri', 'Sokoto',
    'Ilorin', 'Enugu', 'Abeokuta', 'Owerri', 'Calabar'
  ];

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await apiService.getRecentAlerts(100);
      setAlerts(response.data.alerts || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch alerts:', err);
      setError('Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setAlertForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const sendBulkAlert = async (e) => {
    e.preventDefault();
    
    if (!alertForm.message.trim()) {
      setError('Please enter an alert message');
      return;
    }

    try {
      setSendingAlert(true);
      setError(null);
      
      const response = await apiService.sendBulkAlert(
        alertForm.region,
        alertForm.message,
        alertForm.severityThreshold
      );

      if (response.data.status === 'completed') {
        alert(`Alert sent successfully to ${response.data.sent} users in ${alertForm.region}`);
        setAlertForm(prev => ({ ...prev, message: '' }));
        fetchAlerts(); // Refresh alerts list
      } else if (response.data.status === 'no_users') {
        alert(response.data.message);
      }
      
    } catch (err) {
      console.error('Failed to send alert:', err);
      setError('Failed to send alert. Please try again.');
    } finally {
      setSendingAlert(false);
    }
  };

  const sendEmergencyAlert = async (region) => {
    const emergencyMessage = `🚨 EMERGENCY FLOOD WARNING - ${region}
    
IMMEDIATE EVACUATION REQUIRED
- Move to higher ground immediately
- Follow designated evacuation routes
- Take essential items only
- Stay calm and help others

This is an automated emergency alert from FloodGuardian AI.`;

    try {
      setSendingAlert(true);
      await apiService.sendBulkAlert(region, emergencyMessage, 0.8);
      alert(`Emergency alert sent to all users in ${region}`);
      fetchAlerts();
    } catch (err) {
      setError('Failed to send emergency alert');
    } finally {
      setSendingAlert(false);
    }
  };

  return (
    <div className="alerts-page">
      <div className="alerts-header">
        <h1>Alert Management</h1>
        <p>Send emergency notifications and manage alert history</p>
      </div>

      <div className="grid grid-cols-2">
        {/* Send Alert Form */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Send Alert</h2>
          </div>

          {error && (
            <div className="error">
              <p>{error}</p>
            </div>
          )}

          <form onSubmit={sendBulkAlert} className="alert-form">
            <div className="form-group">
              <label htmlFor="region">Target Region</label>
              <select
                id="region"
                name="region"
                value={alertForm.region}
                onChange={handleInputChange}
                className="form-control"
              >
                {nigerianRegions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="message">Alert Message</label>
              <textarea
                id="message"
                name="message"
                value={alertForm.message}
                onChange={handleInputChange}
                className="form-control"
                rows="4"
                placeholder="Enter your alert message here..."
                required
              />
              <small className="form-help">
                Keep messages clear and actionable. Include specific instructions.
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="severityThreshold">Severity Threshold</label>
              <select
                id="severityThreshold"
                name="severityThreshold"
                value={alertForm.severityThreshold}
                onChange={handleInputChange}
                className="form-control"
              >
                <option value={0.3}>Low Risk (0.3+)</option>
                <option value={0.5}>Medium Risk (0.5+)</option>
                <option value={0.7}>High Risk (0.7+)</option>
                <option value={0.9}>Critical Risk (0.9+)</option>
              </select>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={sendingAlert}
              >
                {sendingAlert ? 'Sending...' : 'Send Alert'}
              </button>
            </div>
          </form>
        </div>

        {/* Quick Emergency Alerts */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Emergency Alerts</h2>
          </div>

          <div className="emergency-alerts">
            <p className="emergency-description">
              Send immediate emergency alerts to all users in a region.
            </p>

            <div className="emergency-regions">
              {nigerianRegions.slice(0, 8).map(region => (
                <button
                  key={region}
                  className="btn btn-danger emergency-btn"
                  onClick={() => sendEmergencyAlert(region)}
                  disabled={sendingAlert}
                >
                  🚨 Alert {region}
                </button>
              ))}
            </div>

            <div className="emergency-warning">
              <p>⚠️ Emergency alerts will be sent to ALL registered users in the selected region.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Alerts History */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Recent Alerts</h2>
          <button 
            className="btn btn-secondary"
            onClick={fetchAlerts}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>

        {loading && alerts.length === 0 ? (
          <div className="loading">Loading alerts...</div>
        ) : (
          <div className="alerts-table">
            <div className="table-header">
              <span>Message</span>
              <span>User</span>
              <span>Region</span>
              <span>Sent At</span>
            </div>

            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <div key={alert.id} className="table-row">
                  <span className="message-cell">
                    {alert.message.length > 100 
                      ? `${alert.message.substring(0, 100)}...` 
                      : alert.message
                    }
                  </span>
                  <span className="user-cell">
                    {alert.users?.name || `User #${alert.user_id}`}
                  </span>
                  <span className="region-cell">
                    {alert.users?.location || 'N/A'}
                  </span>
                  <span className="time-cell">
                    {new Date(alert.sent_at).toLocaleString()}
                  </span>
                </div>
              ))
            ) : (
              <div className="no-data">
                <p>No alerts found</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Alerts;

