import requests
from typing import Dict, List, Any
from config import MAPS_API_KEY

class RoutingService:
    """
    Service to provide evacuation routes using OpenRouteService (free alternative to Google Maps)
    """
    
    def __init__(self):
        self.api_key = MAPS_API_KEY
        # Use OpenRouteService instead of Google Maps (free tier available)
        self.base_url = "https://api.openrouteservice.org/v2"
    
    def get_evacuation_route(self, origin: str, destination: str = None, region: str = None) -> Dict[str, Any]:
        """
        Get evacuation route from origin to safe destination
        
        Args:
            origin: Starting point (address or coordinates)
            destination: Safe destination (optional)
            region: Region name for context (optional)
            
        Returns:
            Dict containing route information
        """
        try:
            # For now, use mock data since we don't have a routing API key
            # In production, you could use OpenRouteService (free tier) or other alternatives
            return self._get_mock_route(origin, destination or "Safe Zone")
            
            # Future implementation with OpenRouteService:
            # if not self.api_key or self.api_key == "your-maps-api-key":
            #     return self._get_mock_route(origin, destination or "Safe Zone")
            # 
            # # If no destination provided, find nearest evacuation center
            # if not destination:
            #     destination = self._find_nearest_evacuation_center(origin, region)
            # 
            # headers = {"Authorization": f"Bearer {self.api_key}"}
            # body = {
            #     "coordinates": [[origin_lng, origin_lat], [dest_lng, dest_lat]],
            #     "profile": "driving-car",
            #     "format": "json"
            # }
            # 
            # url = f"{self.base_url}/directions/driving-car/json"
            # response = requests.post(url, json=body, headers=headers)
            # 
            # if response.status_code == 200:
            #     data = response.json()
            #     return self._process_ors_route_response(data)
            # else:
            #     return {"error": f"Routing API failed with status {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Routing service error: {str(e)}"}
    
    def get_multiple_evacuation_routes(self, origins: List[str], region: str) -> List[Dict[str, Any]]:
        """
        Get evacuation routes for multiple origins
        """
        routes = []
        for origin in origins:
            route = self.get_evacuation_route(origin, region=region)
            routes.append(route)
        return routes
    
    def _find_nearest_evacuation_center(self, origin: str, region: str = None) -> str:
        """
        Find the nearest evacuation center (placeholder implementation)
        """
        # In a real implementation, this would query a database of evacuation centers
        evacuation_centers = {
            "Abuja": "National Stadium, Abuja",
            "Lagos": "Tafawa Balewa Square, Lagos",
            "Kano": "Sani Abacha Stadium, Kano",
            "Port Harcourt": "Liberation Stadium, Port Harcourt"
        }
        
        return evacuation_centers.get(region, "Nearest Safe Zone")
    
    def _process_route_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Google Maps API response into our format
        """
        if data.get("status") != "OK" or not data.get("routes"):
            return {"error": "No routes found"}
        
        route = data["routes"][0]  # Get the first route
        leg = route["legs"][0]
        
        return {
            "status": "success",
            "distance": leg["distance"]["text"],
            "duration": leg["duration"]["text"],
            "start_address": leg["start_address"],
            "end_address": leg["end_address"],
            "steps": [step["html_instructions"] for step in leg["steps"]],
            "polyline": route["overview_polyline"]["points"]
        }
    
    def _get_mock_route(self, origin: str, destination: str) -> Dict[str, Any]:
        """
        Mock route data for development/testing
        """
        import random
        
        return {
            "status": "success",
            "distance": f"{random.randint(5, 50)} km",
            "duration": f"{random.randint(10, 90)} mins",
            "start_address": origin,
            "end_address": destination,
            "steps": [
                "Head north on Main Street",
                "Turn right onto Highway 1",
                "Continue for 15 km",
                "Turn left to evacuation center",
                "Arrive at destination"
            ],
            "polyline": "mock_polyline_data_here"
        }

# Create a global instance
routing_service = RoutingService()
