from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.routing_service import routing_service

router = APIRouter()

class RouteRequest(BaseModel):
    origin: str
    destination: str = None
    region: str = None

class BulkRouteRequest(BaseModel):
    origins: List[str]
    region: str

@router.post("/evacuation")
def get_evacuation_route(route_request: RouteRequest) -> Dict[str, Any]:
    """
    Get evacuation route from origin to safe destination
    
    Args:
        route_request: Route request containing origin, optional destination and region
        
    Returns:
        Route information including distance, duration, and steps
    """
    try:
        route_data = routing_service.get_evacuation_route(
            origin=route_request.origin,
            destination=route_request.destination,
            region=route_request.region
        )
        
        if "error" in route_data:
            raise HTTPException(status_code=500, detail=route_data["error"])
        
        return {
            "status": "success",
            "route": route_data,
            "request": {
                "origin": route_request.origin,
                "destination": route_request.destination,
                "region": route_request.region
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing service error: {str(e)}")

@router.post("/evacuation/bulk")
def get_bulk_evacuation_routes(bulk_request: BulkRouteRequest) -> Dict[str, Any]:
    """
    Get evacuation routes for multiple origins
    
    Args:
        bulk_request: Bulk route request containing list of origins and region
        
    Returns:
        List of routes for each origin
    """
    try:
        routes = routing_service.get_multiple_evacuation_routes(
            origins=bulk_request.origins,
            region=bulk_request.region
        )
        
        successful_routes = [route for route in routes if "error" not in route]
        failed_routes = [route for route in routes if "error" in route]
        
        return {
            "status": "completed",
            "region": bulk_request.region,
            "total_requests": len(bulk_request.origins),
            "successful_routes": successful_routes,
            "failed_routes": failed_routes,
            "success_count": len(successful_routes),
            "failure_count": len(failed_routes)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk routing service error: {str(e)}")

@router.get("/evacuation-centers/{region}")
def get_evacuation_centers(region: str) -> Dict[str, Any]:
    """
    Get available evacuation centers for a region
    
    Args:
        region: Region name
        
    Returns:
        List of evacuation centers
    """
    try:
        # This would typically query a database of evacuation centers
        # For now, return mock data
        evacuation_centers = {
            "Abuja": [
                {"name": "National Stadium", "address": "National Stadium, Abuja", "capacity": 10000},
                {"name": "University of Abuja", "address": "Airport Road, Abuja", "capacity": 5000},
                {"name": "Abuja Municipal Area Council", "address": "AMAC Secretariat", "capacity": 3000}
            ],
            "Lagos": [
                {"name": "National Theatre", "address": "Iganmu, Lagos", "capacity": 8000},
                {"name": "Tafawa Balewa Square", "address": "Lagos Island", "capacity": 15000},
                {"name": "University of Lagos", "address": "Akoka, Lagos", "capacity": 12000}
            ],
            "Kano": [
                {"name": "Sani Abacha Stadium", "address": "Kano", "capacity": 25000},
                {"name": "Bayero University", "address": "New Site, Kano", "capacity": 8000}
            ],
            "Port Harcourt": [
                {"name": "Liberation Stadium", "address": "Port Harcourt", "capacity": 38000},
                {"name": "University of Port Harcourt", "address": "Choba, Port Harcourt", "capacity": 10000}
            ]
        }
        
        centers = evacuation_centers.get(region, [])
        
        return {
            "status": "success",
            "region": region,
            "evacuation_centers": centers,
            "count": len(centers)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get evacuation centers: {str(e)}")

@router.get("/traffic/{region}")
def get_traffic_conditions(region: str) -> Dict[str, Any]:
    """
    Get current traffic conditions for evacuation planning
    
    Args:
        region: Region name
        
    Returns:
        Traffic conditions information
    """
    try:
        # Mock traffic data - in production, integrate with traffic APIs
        import random
        
        traffic_conditions = {
            "region": region,
            "overall_status": random.choice(["light", "moderate", "heavy"]),
            "major_routes": [
                {
                    "route_name": f"Highway A1 - {region}",
                    "status": random.choice(["clear", "slow", "congested"]),
                    "estimated_delay": f"{random.randint(0, 45)} minutes"
                },
                {
                    "route_name": f"Main Street - {region}",
                    "status": random.choice(["clear", "slow", "congested"]),
                    "estimated_delay": f"{random.randint(0, 30)} minutes"
                }
            ],
            "recommended_departure_time": "Immediately for high-risk areas",
            "last_updated": "2025-09-11T21:30:00Z"
        }
        
        return {
            "status": "success",
            "traffic": traffic_conditions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get traffic conditions: {str(e)}")

