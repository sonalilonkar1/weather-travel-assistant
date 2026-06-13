import json
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import io
import logging

from database import get_db, init_db
from models import SavedLocation, WeatherRequest
from schemas import (
    WeatherData, SavedLocationCreate, SavedLocationUpdate, YouTubeVideo,
    SavedLocationResponse, LocationData, ForecastDay, WeatherRequestCreate, WeatherRequestUpdate
)

from database import get_db
from models import WeatherRequest
from export_service import (
    export_weather_requests_json,
    export_weather_requests_csv,
    export_weather_requests_pdf,
)

from crud import (
    create_weather_request,
    list_weather_requests,
    get_weather_request,
    update_weather_request,
    delete_weather_request
)

from services import WeatherService, GeocodingService, YouTubeService
from config import HOST, PORT, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.INFO if not DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Weather Travel Assistant API",
    description="Real-time weather data API with location management",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # Alternative docs
)

# CORS configuration - allows frontend to call from localhost:5173
# Need to restrict to specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: ["http://localhost:3000", "https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Convert WeatherRequest database record into JSON response.
def serialize_weather_request(record):
    return {
        "id": record.id,
        "location_query": record.location_query,
        "resolved_location": record.resolved_location,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "start_date": record.start_date,
        "end_date": record.end_date,
        "current_weather": json.loads(record.current_weather),
        "forecast_data": json.loads(record.forecast_data),
        "hourly_forecast": json.loads(record.hourly_forecast) if record.hourly_forecast else [],
        "travel_tips": json.loads(record.travel_tips) if record.travel_tips else [],
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }

# Initialize database tables on app startup
@app.on_event("startup")
def startup_event():
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# ==================== WEATHER ENDPOINTS ====================

# Get current weather for given coordinates.
@app.get("/api/weather/current", response_model=WeatherData)
async def get_current_weather(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)")
):
    try:
        logger.debug(f"Fetching weather for coordinates: {latitude}, {longitude}")
        weather = await WeatherService.get_current_weather(latitude, longitude)
        logger.info(f"Successfully fetched weather for ({latitude}, {longitude})")
        return weather
    except ValueError as e:
        logger.warning(f"Invalid coordinate input: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid coordinates: {str(e)}")
    except Exception as e:
        logger.error(f"Weather service error: {e}")
        raise HTTPException(
            status_code=503, 
            detail="Weather service unavailable. Please try again later."
        )


# Get 5-day weather forecast for given coordinates.
@app.get("/api/weather/forecast")
async def get_forecast(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)")
):
    try:
        logger.debug(f"Fetching 5-day forecast for: {latitude}, {longitude}")
        forecast = await WeatherService.get_forecast(latitude, longitude)
        return {"forecast": forecast}
    except ValueError as e:
        logger.warning(f"Invalid forecast request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Forecast service error: {e}")
        raise HTTPException(status_code=503, detail="Forecast service temporarily unavailable")



# ==================== GEOCODING ENDPOINTS ====================

# Convert location string to coordinates
@app.get("/api/geocode", response_model=LocationData)
async def geocode_location(location: str = Query(..., description="Location name or coordinates")):
    try:
        result = await GeocodingService.geocode_location(location)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Convert coordinates to location name
@app.get("/api/reverse-geocode", response_model=LocationData)
async def reverse_geocode(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude")
):
    try:
        result = await GeocodingService.reverse_geocode(latitude, longitude)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== YOUTUBE VIDEOS ENDPOINT ====================

# Get YouTube videos related to a location
@app.get("/api/videos", response_model=list[YouTubeVideo])
async def get_location_videos(location: str = Query(..., min_length=1)):
    try:
        videos = await YouTubeService.search_location_videos(location)
        return videos
    except Exception as e:
        logger.error(f"Error fetching YouTube videos: {e}")
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch location videos right now."
        )

# ==================== SAVED LOCATIONS CRUD ====================

# Get all saved locations, ordered by most recent.
@app.get("/api/locations", response_model=List[SavedLocationResponse])
def list_locations(db: Session = Depends(get_db)):
    try:
        logger.debug("Fetching all saved locations")
        locations = db.query(SavedLocation)\
            .order_by(SavedLocation.created_at.desc())\
            .all()
        logger.info(f"Retrieved {len(locations)} saved locations")
        return locations
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to retrieve saved locations"
        )

# Create a new saved location
@app.post("/api/locations", response_model=SavedLocationResponse)
def create_location(
    location_data: SavedLocationCreate,
    db: Session = Depends(get_db)
):
    try:
        # Validate coordinates before saving
        if not (-90 <= location_data.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= location_data.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        logger.debug(f"Saving location: {location_data.location}")
        
        db_location = SavedLocation(
            location=location_data.location.strip(),
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            temperature=location_data.temperature,
            description=location_data.description,
            icon=location_data.icon or "0"
        )
        
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        
        logger.info(f"Successfully saved location: {location_data.location} (ID: {db_location.id})")
        return db_location
        
    except ValueError as e:
        logger.warning(f"Invalid location data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save location: {e}")
        raise HTTPException(status_code=500, detail="Failed to save location")


# Get a specific saved location by ID
@app.get("/api/locations/{location_id}", response_model=SavedLocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Fetching location ID: {location_id}")
        location = db.query(SavedLocation)\
            .filter(SavedLocation.id == location_id)\
            .first()
        
        if not location:
            logger.warning(f"Location not found: {location_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"Location with ID {location_id} not found"
            )
        
        return location
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching location {location_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch location")


# Update a saved location by ID (partial update)
@app.put("/api/locations/{location_id}", response_model=SavedLocationResponse)
def update_location(
    location_id: int,
    update_data: SavedLocationUpdate,
    db: Session = Depends(get_db)
):
    try:
        location = db.query(SavedLocation)\
            .filter(SavedLocation.id == location_id)\
            .first()
        
        if not location:
            raise HTTPException(
                status_code=404, 
                detail=f"Location with ID {location_id} not found"
            )
        
        logger.debug(f"Updating location {location_id}")
        
        # Only update provided fields
        update_fields = update_data.dict(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(location, field, value)
        
        db.commit()
        db.refresh(location)
        
        logger.info(f"Updated location {location_id}")
        return location
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update location {location_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update location")


# Delete a saved location by ID
@app.delete("/api/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    try:
        location = db.query(SavedLocation)\
            .filter(SavedLocation.id == location_id)\
            .first()
        
        if not location:
            raise HTTPException(
                status_code=404, 
                detail=f"Location with ID {location_id} not found"
            )
        
        logger.debug(f"Deleting location {location_id}")
        db.delete(location)
        db.commit()
        
        logger.info(f"Successfully deleted location {location_id}")
        return {
            "message": f"Location {location_id} deleted successfully",
            "deleted_location": location.location
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete location {location_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete location")


# ==================== EXPORT ENDPOINTS ====================

# Export weather requests in JSON, CSV, or PDF format
@app.get("/api/weather-requests/export")
async def export_weather_requests(
    format: str = Query("json"),
    db: Session = Depends(get_db),
):
    export_format = format.lower()

    if export_format not in ["json", "csv", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported export format. Use json, csv, or pdf.",
        )

    requests = (
        db.query(WeatherRequest)
        .order_by(WeatherRequest.created_at.desc())
        .all()
    )

    timestamp = datetime.now().strftime("%Y-%m-%d")

    if export_format == "json":
        content = export_weather_requests_json(requests)
        media_type = "application/json"
        filename = f"weather-requests-{timestamp}.json"

    elif export_format == "csv":
        content = export_weather_requests_csv(requests)
        media_type = "text/csv"
        filename = f"weather-requests-{timestamp}.csv"

    else:
        content = export_weather_requests_pdf(requests)
        media_type = "application/pdf"
        filename = f"weather-requests-{timestamp}.pdf"

    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )

# ==================== WEATHER REQUEST CRUD ====================

# Create a new weather request with current weather, forecast, and travel tips
@app.post("/api/weather-requests")
async def create_weather_request_endpoint(
    request: WeatherRequestCreate,
    db: Session = Depends(get_db)
):
    try:
        record = await create_weather_request(db, request)
        return serialize_weather_request(record)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create weather request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# List all weather requests, ordered by most recent.
@app.get("/api/weather-requests")
def list_weather_requests_endpoint(db: Session = Depends(get_db)):
    records = list_weather_requests(db)
    return [serialize_weather_request(record) for record in records]


# Get a specific weather request by ID
@app.get("/api/weather-requests/{request_id}")
def get_weather_request_endpoint(
    request_id: int,
    db: Session = Depends(get_db)
):
    record = get_weather_request(db, request_id)
    return serialize_weather_request(record)


# Update a weather request by ID (partial update)
@app.put("/api/weather-requests/{request_id}")
async def update_weather_request_endpoint(
    request_id: int,
    request: WeatherRequestUpdate,
    db: Session = Depends(get_db)
):
    try:
        record = await update_weather_request(db, request_id, request)
        return serialize_weather_request(record)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update weather request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Delete a weather request by ID
@app.delete("/api/weather-requests/{request_id}")
def delete_weather_request_endpoint(
    request_id: int,
    db: Session = Depends(get_db)
):
    return delete_weather_request(db, request_id)


# ==================== HEALTH & INFO ENDPOINTS ====================
# health check endpoint for monitoring
@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Weather Travel Assistant API"
    }

# Root endpoint with API information
@app.get("/")
def root_info():
    """Root endpoint with API information"""
    return {
        "name": "Weather Travel Assistant API",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/api/health",
        "endpoints": {
            "weather": "/api/weather/current, /api/weather/forecast",
            "geocoding": "/api/geocode, /api/reverse-geocode",
            "locations": "/api/locations (CRUD)",
            "export": "/api/export?format=json|csv|markdown"
        }
    }


# ==================== ERROR HANDLERS ====================
# Custom HTTP exception handler with logging
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )


# ==================== APP STARTUP INFO ====================
# App entry point with startup logging
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting Weather Travel Assistant API")
    logger.info(f"Server: {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Docs available at: http://{HOST}:{PORT}/docs")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="debug" if DEBUG else "info"
    )
