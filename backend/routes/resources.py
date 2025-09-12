from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.resource_allocator import resource_allocator

router = APIRouter()

class ResourceAllocationRequest(BaseModel):
    region: str
    affected_population: int = None
    severity: float = 0.5

class ResourceUpdateRequest(BaseModel):
    region: str
    resource_type: str
    quantity: int
    action: str = "allocate"  # allocate, distribute, request

@router.post("/allocate")
def allocate_resources(request: ResourceAllocationRequest) -> Dict[str, Any]:
    """
    Allocate resources for a region based on flood prediction
    
    Args:
        request: Resource allocation request
        
    Returns:
        Resource allocation details
    """
    try:
        allocation = resource_allocator.allocate_resources(
            region=request.region,
            affected_population=request.affected_population,
            severity=request.severity
        )
        
        if "error" in allocation:
            raise HTTPException(status_code=500, detail=allocation["error"])
        
        return {
            "status": "success",
            "allocation": allocation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resource allocation error: {str(e)}")

@router.get("/status/{region}")
def get_resource_status(region: str) -> Dict[str, Any]:
    """
    Get current resource status for a region
    
    Args:
        region: Region name
        
    Returns:
        Current resource allocation and availability
    """
    try:
        status = resource_allocator.get_resource_status(region)
        
        return {
            "status": "success",
            "region": region,
            "resources": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get resource status: {str(e)}")

@router.post("/update")
def update_resource_inventory(update: ResourceUpdateRequest) -> Dict[str, Any]:
    """
    Update resource inventory (allocate, distribute, or request more)
    
    Args:
        update: Resource update request
        
    Returns:
        Update confirmation
    """
    try:
        from database import supabase
        
        # Record the resource update
        update_record = {
            "region": update.region,
            "resource_type": update.resource_type,
            "quantity": update.quantity,
            "action": update.action
        }
        
        result = supabase.table("resources").insert(update_record).execute()
        
        return {
            "status": "success",
            "update": update_record,
            "database_id": result.data[0]["id"] if result.data else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update resources: {str(e)}")

@router.get("/inventory")
def get_global_inventory() -> Dict[str, Any]:
    """
    Get global resource inventory across all regions
    
    Returns:
        Global resource status
    """
    try:
        from database import supabase
        
        # Get all resource records
        result = supabase.table("resources").select("*").execute()
        
        # Aggregate by region and resource type
        inventory = {}
        for record in result.data:
            region = record["region"]
            resource_type = record["resource_type"]
            
            if region not in inventory:
                inventory[region] = {}
            
            if resource_type not in inventory[region]:
                inventory[region][resource_type] = {
                    "total_allocated": 0,
                    "total_distributed": 0,
                    "available": 0
                }
            
            # This is a simplified aggregation - in practice, you'd want more sophisticated tracking
            inventory[region][resource_type]["total_allocated"] += record["quantity"]
        
        return {
            "status": "success",
            "inventory": inventory,
            "total_regions": len(inventory)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get inventory: {str(e)}")

@router.get("/requirements/{region}")
def get_resource_requirements(region: str, population: int = None) -> Dict[str, Any]:
    """
    Get resource requirements for a region based on population
    
    Args:
        region: Region name
        population: Affected population (optional)
        
    Returns:
        Resource requirements breakdown
    """
    try:
        if not population:
            # Estimate population based on region
            regional_populations = {
                "Abuja": 500000,
                "Lagos": 2000000,
                "Kano": 800000,
                "Port Harcourt": 600000,
                "Ibadan": 700000,
                "Kaduna": 400000
            }
            population = regional_populations.get(region, 100000)
        
        # Calculate requirements using the resource allocator logic
        allocation = resource_allocator.allocate_resources(region, population, 0.8)  # High severity
        
        if "error" in allocation:
            raise HTTPException(status_code=500, detail=allocation["error"])
        
        return {
            "status": "success",
            "region": region,
            "population": population,
            "requirements": allocation["resources"],
            "estimated_cost": allocation["total_cost_estimate"],
            "priority": allocation["priority"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get requirements: {str(e)}")

