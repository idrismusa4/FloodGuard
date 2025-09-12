import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),
  
  // Dashboard stats
  getDashboardStats: () => api.get('/dashboard/stats'),
  
  // Predictions
  getPrediction: (region, lat = null, lon = null) => {
    const params = {};
    if (lat !== null) params.lat = lat;
    if (lon !== null) params.lon = lon;
    return api.get(`/predictions/${region}`, { params });
  },
  
  getPredictionHistory: (region, limit = 10) => 
    api.get(`/predictions/history/${region}`, { params: { limit } }),
  
  getAllRecentPredictions: (limit = 20) => 
    api.get('/predictions', { params: { limit } }),
  
  // Alerts
  sendAlert: (userId, message) => 
    api.post('/alerts/send', { user_id: userId, message }),
  
  sendBulkAlert: (region, message, severityThreshold = 0.5) => 
    api.post('/alerts/bulk', { 
      region, 
      message, 
      severity_threshold: severityThreshold 
    }),
  
  getAlertHistory: (userId, limit = 10) => 
    api.get(`/alerts/history/${userId}`, { params: { limit } }),
  
  getRecentAlerts: (limit = 50) => 
    api.get('/alerts', { params: { limit } }),
  
  // Routes
  getEvacuationRoute: (origin, destination = null, region = null) => 
    api.post('/routes/evacuation', { origin, destination, region }),
  
  getBulkEvacuationRoutes: (origins, region) => 
    api.post('/routes/evacuation/bulk', { origins, region }),
  
  getEvacuationCenters: (region) => 
    api.get(`/routes/evacuation-centers/${region}`),
  
  getTrafficConditions: (region) => 
    api.get(`/routes/traffic/${region}`),
  
  // Resources
  allocateResources: (region, affectedPopulation = null, severity = 0.5) => 
    api.post('/resources/allocate', { 
      region, 
      affected_population: affectedPopulation, 
      severity 
    }),
  
  getResourceStatus: (region) => 
    api.get(`/resources/status/${region}`),
  
  updateResourceInventory: (region, resourceType, quantity, action = 'allocate') => 
    api.post('/resources/update', { 
      region, 
      resource_type: resourceType, 
      quantity, 
      action 
    }),
  
  getGlobalInventory: () => 
    api.get('/resources/inventory'),
  
  getResourceRequirements: (region, population = null) => 
    api.get(`/resources/requirements/${region}`, { 
      params: population ? { population } : {} 
    }),
};

// Utility functions
export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString();
};

export const formatSeverity = (severity) => {
  if (severity >= 0.7) return { level: 'HIGH', color: 'status-high' };
  if (severity >= 0.4) return { level: 'MEDIUM', color: 'status-medium' };
  return { level: 'LOW', color: 'status-low' };
};

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

export const formatNumber = (number) => {
  return new Intl.NumberFormat('en-US').format(number);
};

export default api;

