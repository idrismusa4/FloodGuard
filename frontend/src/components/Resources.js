import React, { useState, useEffect } from 'react';
import { apiService, formatCurrency, formatNumber } from '../services/api';
import './Resources.css';

const Resources = () => {
  const [selectedRegion, setSelectedRegion] = useState('Abuja');
  const [allocation, setAllocation] = useState(null);
  const [inventory, setInventory] = useState({});
  const [requirements, setRequirements] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const nigerianRegions = [
    'Abuja', 'Lagos', 'Kano', 'Port Harcourt', 'Ibadan', 
    'Kaduna', 'Benin City', 'Jos', 'Maiduguri', 'Sokoto',
    'Ilorin', 'Enugu', 'Abeokuta', 'Owerri', 'Calabar'
  ];

  const resourceIcons = {
    food_packets: '🍱',
    water_bottles: '💧',
    medical_kits: '🏥',
    blankets: '🛏️',
    rescue_boats: '🚤',
    shelters: '🏕️'
  };

  useEffect(() => {
    fetchGlobalInventory();
    if (selectedRegion) {
      fetchRegionRequirements(selectedRegion);
    }
  }, [selectedRegion]);

  const fetchGlobalInventory = async () => {
    try {
      const response = await apiService.getGlobalInventory();
      setInventory(response.data.inventory || {});
    } catch (err) {
      console.error('Failed to fetch inventory:', err);
    }
  };

  const fetchRegionRequirements = async (region) => {
    try {
      const response = await apiService.getResourceRequirements(region);
      setRequirements(response.data);
    } catch (err) {
      console.error('Failed to fetch requirements:', err);
    }
  };

  const allocateResources = async (severity = 0.8) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiService.allocateResources(
        selectedRegion,
        null, // Let the system estimate population
        severity
      );
      
      setAllocation(response.data.allocation);
      await fetchGlobalInventory(); // Refresh inventory
      
    } catch (err) {
      console.error('Failed to allocate resources:', err);
      setError('Failed to allocate resources');
    } finally {
      setLoading(false);
    }
  };

  const handleRegionChange = (region) => {
    setSelectedRegion(region);
    setAllocation(null); // Clear previous allocation
  };

  return (
    <div className="resources-page">
      <div className="resources-header">
        <h1>Resource Management</h1>
        <p>Allocate and track emergency resources across regions</p>
      </div>

      <div className="grid grid-cols-3">
        {/* Region Selector & Actions */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Select Region</h2>
          </div>
          
          <div className="region-selector">
            <select
              value={selectedRegion}
              onChange={(e) => handleRegionChange(e.target.value)}
              className="form-control region-select"
            >
              {nigerianRegions.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
          </div>

          <div className="allocation-actions">
            <button
              className="btn btn-primary allocation-btn"
              onClick={() => allocateResources(0.5)}
              disabled={loading}
            >
              {loading ? 'Allocating...' : 'Standard Allocation'}
            </button>
            
            <button
              className="btn btn-danger allocation-btn"
              onClick={() => allocateResources(0.9)}
              disabled={loading}
            >
              {loading ? 'Allocating...' : 'Emergency Allocation'}
            </button>
          </div>

          {error && (
            <div className="error">
              <p>{error}</p>
            </div>
          )}
        </div>

        {/* Resource Requirements */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Requirements - {selectedRegion}</h2>
          </div>
          
          {requirements ? (
            <div className="requirements-content">
              <div className="requirements-summary">
                <div className="summary-item">
                  <label>Population</label>
                  <value>{formatNumber(requirements.population)}</value>
                </div>
                <div className="summary-item">
                  <label>Estimated Cost</label>
                  <value>{formatCurrency(requirements.estimated_cost)}</value>
                </div>
                <div className="summary-item">
                  <label>Priority</label>
                  <value className={`priority-${requirements.priority}`}>
                    {requirements.priority.toUpperCase()}
                  </value>
                </div>
              </div>

              <div className="requirements-list">
                {Object.entries(requirements.requirements || {}).map(([resource, quantity]) => (
                  <div key={resource} className="requirement-item">
                    <span className="resource-icon">
                      {resourceIcons[resource] || '📦'}
                    </span>
                    <span className="resource-name">
                      {resource.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                    <span className="resource-quantity">
                      {formatNumber(quantity)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="loading">Loading requirements...</div>
          )}
        </div>

        {/* Current Allocation */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Current Allocation</h2>
          </div>
          
          {allocation ? (
            <div className="allocation-content">
              <div className="allocation-summary">
                <div className="summary-metric">
                  <h3>{formatNumber(allocation.affected_population)}</h3>
                  <p>Affected Population</p>
                </div>
                <div className="summary-metric">
                  <h3>{formatCurrency(allocation.total_cost_estimate)}</h3>
                  <p>Total Cost</p>
                </div>
                <div className="summary-metric">
                  <h3 className={`priority-${allocation.priority}`}>
                    {allocation.priority.toUpperCase()}
                  </h3>
                  <p>Priority Level</p>
                </div>
              </div>

              <div className="allocated-resources">
                {Object.entries(allocation.resources || {}).map(([resource, quantity]) => (
                  <div key={resource} className="allocated-item">
                    <span className="resource-icon">
                      {resourceIcons[resource] || '📦'}
                    </span>
                    <div className="resource-details">
                      <span className="resource-name">
                        {resource.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </span>
                      <span className="resource-quantity">
                        {formatNumber(quantity)} units
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="no-allocation">
              <p>Select allocation type above to see resource distribution</p>
            </div>
          )}
        </div>
      </div>

      {/* Global Inventory */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Global Resource Inventory</h2>
          <button 
            className="btn btn-secondary"
            onClick={fetchGlobalInventory}
          >
            Refresh
          </button>
        </div>
        
        <div className="inventory-grid">
          {Object.keys(inventory).length > 0 ? (
            Object.entries(inventory).map(([region, resources]) => (
              <div key={region} className="inventory-region">
                <h3 className="region-name">{region}</h3>
                <div className="region-resources">
                  {Object.entries(resources).map(([resourceType, data]) => (
                    <div key={resourceType} className="inventory-item">
                      <span className="resource-icon">
                        {resourceIcons[resourceType] || '📦'}
                      </span>
                      <div className="inventory-details">
                        <span className="resource-name">
                          {resourceType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                        <span className="resource-stats">
                          Allocated: {formatNumber(data.total_allocated || 0)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="no-inventory">
              <p>No inventory data available. Allocate resources to regions to see inventory.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Resources;

