from typing import Dict, Any, List
from database import supabase

class ResourceAllocator:
    """
    Service to allocate emergency resources based on flood predictions
    """
    
    def __init__(self):
        self.resource_types = {
            "food_packets": {"unit": "packets", "per_person": 3},
            "water_bottles": {"unit": "bottles", "per_person": 5},
            "medical_kits": {"unit": "kits", "per_100_people": 2},
            "blankets": {"unit": "pieces", "per_person": 1},
            "rescue_boats": {"unit": "boats", "per_1000_people": 1},
            "shelters": {"unit": "tents", "per_10_people": 1}
        }
    
    def allocate_resources(self, region: str, affected_population: int = None, severity: float = 0.5) -> Dict[str, Any]:
        """
        Calculate and allocate resources for a region based on flood severity
        
        Args:
            region: Name of the region
            affected_population: Number of people affected
            severity: Flood severity (0.0 to 1.0)
            
        Returns:
            Dict containing resource allocation details
        """
        try:
            # Estimate affected population if not provided
            if not affected_population:
                affected_population = self._estimate_population(region, severity)
            
            # Calculate resource needs
            resources = self._calculate_resource_needs(affected_population, severity)
            
            # Save allocation to database
            allocation_record = {
                "region": region,
                "affected_population": affected_population,
                "severity": severity,
                "resources": resources,
                "status": "allocated"
            }
            
            # Store in database
            result = supabase.table("resources").insert({
                "region": region,
                "resource_type": "allocation_summary",
                "quantity": affected_population,
                "details": allocation_record
            }).execute()
            
            return {
                "region": region,
                "affected_population": affected_population,
                "severity": severity,
                "resources": resources,
                "total_cost_estimate": self._calculate_cost(resources),
                "priority": "high" if severity > 0.7 else "medium" if severity > 0.4 else "low"
            }
            
        except Exception as e:
            return {"error": f"Resource allocation failed: {str(e)}"}
    
    def _estimate_population(self, region: str, severity: float) -> int:
        """
        Estimate affected population based on region and severity
        """
        # Regional population estimates (simplified)
        regional_populations = {
            "Abuja": 3500000,
            "Lagos": 15000000,
            "Kano": 4000000,
            "Port Harcourt": 2000000,
            "Ibadan": 3500000,
            "Kaduna": 2000000
        }
        
        base_population = regional_populations.get(region, 1000000)
        
        # Estimate affected percentage based on severity
        affected_percentage = min(severity * 0.3, 0.25)  # Max 25% of population
        
        return int(base_population * affected_percentage)
    
    def _calculate_resource_needs(self, population: int, severity: float) -> Dict[str, int]:
        """
        Calculate specific resource quantities needed
        """
        resources = {}
        
        # Adjust quantities based on severity
        severity_multiplier = max(1.0, severity * 1.5)
        
        for resource_type, config in self.resource_types.items():
            if "per_person" in config:
                quantity = int(population * config["per_person"] * severity_multiplier)
            elif "per_100_people" in config:
                quantity = int((population / 100) * config["per_100_people"] * severity_multiplier)
            elif "per_1000_people" in config:
                quantity = int((population / 1000) * config["per_1000_people"] * severity_multiplier)
            elif "per_10_people" in config:
                quantity = int((population / 10) * config["per_10_people"] * severity_multiplier)
            else:
                quantity = int(population * 0.1 * severity_multiplier)
            
            resources[resource_type] = max(1, quantity)  # Ensure at least 1 unit
        
        return resources
    
    def _calculate_cost(self, resources: Dict[str, int]) -> float:
        """
        Estimate total cost of resources (in USD)
        """
        cost_per_unit = {
            "food_packets": 2.0,
            "water_bottles": 0.5,
            "medical_kits": 25.0,
            "blankets": 8.0,
            "rescue_boats": 5000.0,
            "shelters": 150.0
        }
        
        total_cost = 0
        for resource, quantity in resources.items():
            unit_cost = cost_per_unit.get(resource, 10.0)
            total_cost += quantity * unit_cost
        
        return round(total_cost, 2)
    
    def get_resource_status(self, region: str) -> List[Dict[str, Any]]:
        """
        Get current resource allocation status for a region
        """
        try:
            result = supabase.table("resources").select("*").eq("region", region).execute()
            return result.data
        except Exception as e:
            return [{"error": f"Failed to get resource status: {str(e)}"}]

# Create a global instance
resource_allocator = ResourceAllocator()

