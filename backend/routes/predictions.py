from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from services.earth2_service import earth2_service
from database import supabase

router = APIRouter()

@router.get("/{region}")
def get_flood_prediction(region: str, lat: float = None, lon: float = None) -> Dict[str, Any]:
    """
    Get flood prediction for a specific region
    
    Args:
        region: Region name
        lat: Latitude (optional)
        lon: Longitude (optional)
        
    Returns:
        Flood prediction data
    """
    try:
        # Get prediction from Earth-2 service
        prediction_data = earth2_service.get_flood_prediction(region, lat, lon)
        
        if "error" in prediction_data:
            raise HTTPException(status_code=500, detail=prediction_data["error"])
        
        # Save prediction to database
        db_record = {
            "region": region,
            "severity": prediction_data.get("severity", 0.0),
            "prediction_data": prediction_data
        }
        
        try:
            result = supabase.table("predictions").insert(db_record).execute()
            saved_to_db = len(result.data) > 0 if result.data else False
        except Exception as db_error:
            print(f"Database insert failed: {db_error}")
            saved_to_db = False
        
        return {
            "status": "success",
            "region": region,
            "prediction": prediction_data,
            "saved_to_db": saved_to_db
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction service error: {str(e)}")

@router.get("/history/{region}")
def get_prediction_history(region: str, limit: int = 10) -> Dict[str, Any]:
    """
    Get historical predictions for a region
    """
    try:
        result = supabase.table("predictions").select("*").eq("region", region).limit(limit).order("created_at", desc=True).execute()
        
        return {
            "status": "success",
            "region": region,
            "predictions": result.data,
            "count": len(result.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get prediction history: {str(e)}")

@router.get("/")
def get_all_recent_predictions(limit: int = 20) -> Dict[str, Any]:
    """
    Get recent predictions for all regions
    """
    try:
        result = supabase.table("predictions").select("*").limit(limit).order("created_at", desc=True).execute()
        
        return {
            "status": "success",
            "predictions": result.data,
            "count": len(result.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get predictions: {str(e)}")

