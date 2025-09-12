#!/usr/bin/env python3
"""
FloodGuardian AI - Flood Monitoring Job

This is the core job that stitches everything together:
1. Gets predictions from NVIDIA Earth-2
2. Saves predictions to database
3. Sends SMS alerts for high-severity predictions
4. Allocates resources automatically
5. Provides evacuation routes

Run this job periodically (e.g., every hour) via cron or task scheduler.
"""

import time
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.earth2_service import earth2_service
from services.sms_service import sms_service
from services.resource_allocator import resource_allocator
from services.routing_service import routing_service
from database import supabase

class FloodMonitor:
    """
    Main flood monitoring class that orchestrates all services
    """
    
    def __init__(self):
        self.monitored_regions = [
            "Abuja", "Lagos", "Kano", "Port Harcourt", 
            "Ibadan", "Kaduna", "Benin City", "Jos",
            "Maiduguri", "Sokoto", "Ilorin", "Enugu"
        ]
        self.severity_threshold = 0.7  # Threshold for sending alerts
        self.resource_threshold = 0.5  # Threshold for resource allocation
    
    def monitor_all_regions(self):
        """
        Monitor all regions for flood predictions
        """
        print(f"\n🌊 FloodGuardian AI Monitor Started - {datetime.now()}")
        print("=" * 60)
        
        results = {
            "total_regions": len(self.monitored_regions),
            "high_risk_regions": 0,
            "alerts_sent": 0,
            "resources_allocated": 0,
            "errors": []
        }
        
        for region in self.monitored_regions:
            try:
                print(f"\n📍 Monitoring {region}...")
                region_result = self.monitor_region(region)
                
                if region_result["severity"] >= self.severity_threshold:
                    results["high_risk_regions"] += 1
                
                results["alerts_sent"] += region_result.get("alerts_sent", 0)
                if region_result.get("resources_allocated"):
                    results["resources_allocated"] += 1
                    
            except Exception as e:
                error_msg = f"Error monitoring {region}: {str(e)}"
                print(f"❌ {error_msg}")
                results["errors"].append(error_msg)
        
        self.print_summary(results)
        return results
    
    def monitor_region(self, region: str) -> Dict[str, Any]:
        """
        Monitor a specific region for flood risk
        
        Args:
            region: Region name to monitor
            
        Returns:
            Dict containing monitoring results
        """
        result = {
            "region": region,
            "severity": 0.0,
            "alerts_sent": 0,
            "resources_allocated": False,
            "routes_generated": False
        }
        
        try:
            # Step 1: Get flood prediction from Earth-2
            print(f"  🛰️  Getting prediction from Earth-2...")
            prediction = earth2_service.get_flood_prediction(region)
            
            if "error" in prediction:
                print(f"  ⚠️  Earth-2 error: {prediction['error']}")
                return result
            
            severity = prediction.get("severity", 0.0)
            result["severity"] = severity
            
            print(f"  📊 Severity: {severity:.2f} ({'HIGH' if severity > 0.7 else 'MEDIUM' if severity > 0.4 else 'LOW'})")
            
            # Step 2: Save prediction to database
            self.save_prediction(region, prediction)
            print(f"  💾 Prediction saved to database")
            
            # Step 3: Send alerts if severity is high
            if severity >= self.severity_threshold:
                alerts_sent = self.send_region_alerts(region, prediction)
                result["alerts_sent"] = alerts_sent
                print(f"  📱 Sent {alerts_sent} SMS alerts")
            
            # Step 4: Allocate resources if needed
            if severity >= self.resource_threshold:
                self.allocate_region_resources(region, prediction)
                result["resources_allocated"] = True
                print(f"  🚛 Resources allocated")
            
            # Step 5: Generate evacuation routes for high-risk areas
            if severity >= self.severity_threshold:
                self.generate_evacuation_routes(region)
                result["routes_generated"] = True
                print(f"  🗺️  Evacuation routes updated")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            result["error"] = str(e)
        
        return result
    
    def save_prediction(self, region: str, prediction: Dict[str, Any]):
        """
        Save prediction to database
        """
        try:
            record = {
                "region": region,
                "severity": prediction.get("severity", 0.0),
                "prediction_data": prediction
            }
            supabase.table("predictions").insert(record).execute()
        except Exception as e:
            print(f"  ⚠️  Database error: {str(e)}")
    
    def send_region_alerts(self, region: str, prediction: Dict[str, Any]) -> int:
        """
        Send SMS alerts to all users in a region
        
        Returns:
            Number of alerts sent
        """
        try:
            # Get users in the region
            users_result = supabase.table("users").select("*").eq("location", region).execute()
            
            if not users_result.data:
                print(f"  ℹ️  No registered users in {region}")
                return 0
            
            # Create alert message
            severity = prediction.get("severity", 0.0)
            risk_level = "CRITICAL" if severity > 0.8 else "HIGH"
            
            message = f"""
🚨 {risk_level} FLOOD WARNING - {region}
Severity: {severity:.1f}/1.0
Evacuate immediately to higher ground.
Follow evacuation routes provided.
Stay safe! - FloodGuardian AI
            """.strip()
            
            # Send SMS to all users
            alerts_sent = 0
            for user in users_result.data:
                if sms_service.send_sms(user["phone"], message):
                    # Save alert record
                    supabase.table("alerts").insert({
                        "user_id": user["id"],
                        "message": message
                    }).execute()
                    alerts_sent += 1
            
            return alerts_sent
            
        except Exception as e:
            print(f"  ⚠️  Alert error: {str(e)}")
            return 0
    
    def allocate_region_resources(self, region: str, prediction: Dict[str, Any]):
        """
        Allocate emergency resources for a region
        """
        try:
            affected_population = prediction.get("affected_population", 0)
            severity = prediction.get("severity", 0.5)
            
            allocation = resource_allocator.allocate_resources(
                region=region,
                affected_population=affected_population,
                severity=severity
            )
            
            if "error" not in allocation:
                print(f"    💰 Estimated cost: ${allocation['total_cost_estimate']:,.2f}")
                print(f"    👥 Affected population: {allocation['affected_population']:,}")
                
        except Exception as e:
            print(f"  ⚠️  Resource allocation error: {str(e)}")
    
    def generate_evacuation_routes(self, region: str):
        """
        Generate and cache evacuation routes for a region
        """
        try:
            # Get major locations in the region (simplified)
            major_locations = [
                f"City Center, {region}",
                f"Main Market, {region}",
                f"University, {region}",
                f"Airport, {region}"
            ]
            
            routes_generated = 0
            for location in major_locations:
                try:
                    route = routing_service.get_evacuation_route(location, region=region)
                    if "error" not in route:
                        routes_generated += 1
                except:
                    continue
            
            print(f"    🗺️  Generated {routes_generated} evacuation routes")
            
        except Exception as e:
            print(f"  ⚠️  Routing error: {str(e)}")
    
    def print_summary(self, results: Dict[str, Any]):
        """
        Print monitoring summary
        """
        print("\n" + "=" * 60)
        print("📊 MONITORING SUMMARY")
        print("=" * 60)
        print(f"Total Regions Monitored: {results['total_regions']}")
        print(f"High-Risk Regions: {results['high_risk_regions']}")
        print(f"SMS Alerts Sent: {results['alerts_sent']}")
        print(f"Resources Allocated: {results['resources_allocated']}")
        print(f"Errors: {len(results['errors'])}")
        
        if results['errors']:
            print("\n❌ ERRORS:")
            for error in results['errors']:
                print(f"  - {error}")
        
        print(f"\n✅ Monitoring completed at {datetime.now()}")
        print("=" * 60)

def main():
    """
    Main function to run flood monitoring
    """
    monitor = FloodMonitor()
    
    # Check if running in continuous mode
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        print("🔄 Running in continuous mode (every hour)")
        while True:
            try:
                monitor.monitor_all_regions()
                print(f"\n⏰ Waiting 1 hour before next check...")
                time.sleep(3600)  # Wait 1 hour
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                time.sleep(300)  # Wait 5 minutes before retry
    else:
        # Run once
        monitor.monitor_all_regions()

if __name__ == "__main__":
    main()

