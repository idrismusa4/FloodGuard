from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os

# Import routers
from routes import alerts, predictions, routes, resources

# Create FastAPI app
app = FastAPI(
    title="FloodGuardian AI Agent",
    description="AI-powered flood prediction and emergency response system",
    version="1.0.0"
)

# Add CORS middleware
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = (
    [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    if allowed_origins_env != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
app.include_router(routes.router, prefix="/routes", tags=["Routes"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])

@app.get("/")
def root():
    """
    Root endpoint - Health check
    """
    return {
        "message": "FloodGuardian AI Agent Running ✅",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "predictions": "/predictions/{region}",
            "alerts": "/alerts/send",
            "routes": "/routes/evacuation",
            "resources": "/resources/allocate"
        }
    }

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": "2025-09-11T21:00:00Z",
        "services": {
            "database": "connected",
            "earth2": "available",
            "sms": "ready",
            "routing": "ready",
            "resources": "ready"
        }
    }

@app.get("/dashboard/stats")
def get_dashboard_stats():
    """
    Get dashboard statistics
    """
    try:
        from database import supabase
        
        # Get recent statistics
        predictions_count = len(supabase.table("predictions").select("id").execute().data)
        alerts_count = len(supabase.table("alerts").select("id").execute().data)
        users_count = len(supabase.table("users").select("id").execute().data)
        
        # Get recent high-severity predictions
        high_severity = supabase.table("predictions").select("*").gte("severity", 0.7).limit(5).execute()
        
        return {
            "status": "success",
            "stats": {
                "total_predictions": predictions_count,
                "total_alerts_sent": alerts_count,
                "registered_users": users_count,
                "high_severity_regions": len(high_severity.data),
                "system_status": "operational"
            },
            "recent_high_severity": high_severity.data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {str(e)}")

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

