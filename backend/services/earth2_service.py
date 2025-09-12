import requests
import json
from typing import Dict, Any
from config import EARTH2_API_KEY

class Earth2Service:
    """
    Service to interact with NVIDIA Earth-2 Climate Digital Twin API
    """
    
    def __init__(self):
        self.api_key = EARTH2_API_KEY
        self.base_url = "https://api.nvidia.earth2"  # Placeholder URL
    
    def get_flood_prediction(self, region: str, lat: float = None, lon: float = None) -> Dict[str, Any]:
        """
        Get flood prediction for a specific region
        
        Args:
            region: Name of the region
            lat: Latitude (optional)
            lon: Longitude (optional)
            
        Returns:
            Dict containing prediction data
        """
        try:
            # For development, return mock data
            # In production, replace with actual Earth-2 API call
            if (not self.api_key or 
                self.api_key == "your-nvidia-earth2-key" or 
                self.api_key == "mock-earth2-key-for-development"):
                return self._get_mock_prediction(region)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "region": region,
                "forecast_hours": 72,
                "include_flood_risk": True
            }
            
            if lat and lon:
                params.update({"lat": lat, "lon": lon})
            
            url = f"{self.base_url}/predict"
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Earth2 API failed with status {response.status_code}"}
                
        except Exception as e:
            # If API fails, fall back to mock data
            print(f"⚠️ Earth-2 API failed, using mock data: {str(e)}")
            return self._get_mock_prediction(region)
    
    def _get_mock_prediction(self, region: str) -> Dict[str, Any]:
        """
        Mock prediction data for development/testing
        """
        import random
        
        severity = random.uniform(0.1, 1.0)
        
        return {
            "region": region,
            "severity": severity,
            "risk_level": "high" if severity > 0.7 else "medium" if severity > 0.4 else "low",
            "forecast_hours": 72,
            "precipitation_mm": random.uniform(0, 200),
            "water_level_m": random.uniform(0, 5),
            "confidence": random.uniform(0.7, 0.95),
            "affected_population": random.randint(1000, 50000) if severity > 0.5 else 0,
            "timestamp": "2025-09-11T21:00:00Z"
        }

# Create a global instance
earth2_service = Earth2Service()

