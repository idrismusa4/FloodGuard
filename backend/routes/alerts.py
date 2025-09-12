from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.sms_service import sms_service
from database import supabase

router = APIRouter()

class AlertRequest(BaseModel):
    user_id: int
    message: str

class BulkAlertRequest(BaseModel):
    region: str
    message: str
    severity_threshold: float = 0.5

@router.post("/send")
def send_alert(alert: AlertRequest) -> Dict[str, Any]:
    """
    Send alert to a specific user
    
    Args:
        alert: Alert request containing user_id and message
        
    Returns:
        Alert sending status
    """
    try:
        # Get user information from database
        user_result = supabase.table("users").select("*").eq("id", alert.user_id).execute()
        
        if not user_result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = user_result.data[0]
        phone = user["phone"]
        
        # Send SMS
        success = sms_service.send_sms(phone, alert.message)
        
        if success:
            # Save alert to database
            alert_record = {
                "user_id": alert.user_id,
                "message": alert.message
            }
            supabase.table("alerts").insert(alert_record).execute()
        
        return {
            "status": "sent" if success else "failed",
            "user_id": alert.user_id,
            "phone": phone,
            "message": alert.message
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert service error: {str(e)}")

@router.post("/bulk")
def send_bulk_alert(bulk_alert: BulkAlertRequest) -> Dict[str, Any]:
    """
    Send alerts to all users in a region
    
    Args:
        bulk_alert: Bulk alert request
        
    Returns:
        Bulk alert sending status
    """
    try:
        # Get all users in the specified region
        users_result = supabase.table("users").select("*").eq("location", bulk_alert.region).execute()
        
        if not users_result.data:
            return {
                "status": "no_users",
                "message": f"No users found in region: {bulk_alert.region}",
                "sent": 0,
                "failed": 0
            }
        
        # Extract phone numbers
        phone_numbers = [user["phone"] for user in users_result.data]
        
        # Send bulk SMS
        results = sms_service.send_bulk_sms(phone_numbers, bulk_alert.message)
        
        # Save successful alerts to database
        successful_alerts = []
        for user in users_result.data:
            if user["phone"] not in [error.split()[-1] for error in results.get("errors", [])]:
                successful_alerts.append({
                    "user_id": user["id"],
                    "message": bulk_alert.message
                })
        
        if successful_alerts:
            supabase.table("alerts").insert(successful_alerts).execute()
        
        return {
            "status": "completed",
            "region": bulk_alert.region,
            "total_users": len(users_result.data),
            "sent": results["sent"],
            "failed": results["failed"],
            "errors": results.get("errors", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk alert service error: {str(e)}")

@router.get("/history/{user_id}")
def get_alert_history(user_id: int, limit: int = 10) -> Dict[str, Any]:
    """
    Get alert history for a specific user
    """
    try:
        result = supabase.table("alerts").select("*").eq("user_id", user_id).limit(limit).order("sent_at", desc=True).execute()
        
        return {
            "status": "success",
            "user_id": user_id,
            "alerts": result.data,
            "count": len(result.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alert history: {str(e)}")

@router.get("/")
def get_recent_alerts(limit: int = 50) -> Dict[str, Any]:
    """
    Get recent alerts across all users
    """
    try:
        result = supabase.table("alerts").select("*, users(name, location)").limit(limit).order("sent_at", desc=True).execute()
        
        return {
            "status": "success",
            "alerts": result.data,
            "count": len(result.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")

