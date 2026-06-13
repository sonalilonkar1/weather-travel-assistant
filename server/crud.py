import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import WeatherRequest
from schemas import WeatherRequestCreate, WeatherRequestUpdate
from services import GeocodingService, WeatherService
from travel_tips import generate_travel_tips


def _serialize_model(model):
    return model.model_dump()


async def create_weather_request(db: Session, request: WeatherRequestCreate):
    location = await GeocodingService.geocode_location(request.location_query)

    current_weather = await WeatherService.get_current_weather(
        location.latitude,
        location.longitude
    )

    forecast = await WeatherService.get_forecast_for_date_range(
        location.latitude,
        location.longitude,
        str(request.start_date),
        str(request.end_date)
    )
    
    hourly_forecast = await WeatherService.get_hourly_forecast(
        location.latitude,
        location.longitude
    )

    tips = generate_travel_tips(current_weather, forecast)

    db_request = WeatherRequest(
        location_query=request.location_query.strip(),
        resolved_location=f"{location.city}, {location.country}",
        latitude=location.latitude,
        longitude=location.longitude,
        start_date=str(request.start_date),
        end_date=str(request.end_date),
        current_weather=json.dumps(current_weather.model_dump()),
        forecast_data=json.dumps([day.model_dump() for day in forecast]),
        hourly_forecast=json.dumps(hourly_forecast),
        travel_tips=json.dumps(tips)
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request


def list_weather_requests(db: Session):
    return db.query(WeatherRequest).order_by(WeatherRequest.created_at.desc()).all()


def get_weather_request(db: Session, request_id: int):
    db_request = db.query(WeatherRequest).filter(
        WeatherRequest.id == request_id
    ).first()

    if not db_request:
        raise HTTPException(status_code=404, detail="Weather request not found")

    return db_request


async def update_weather_request(
    db: Session,
    request_id: int,
    update_data: WeatherRequestUpdate
):
    db_request = get_weather_request(db, request_id)

    location_query = update_data.location_query or db_request.location_query
    start_date = str(update_data.start_date) if update_data.start_date else db_request.start_date
    end_date = str(update_data.end_date) if update_data.end_date else db_request.end_date

    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date"
        )

    location = await GeocodingService.geocode_location(location_query)

    current_weather = await WeatherService.get_current_weather(
        location.latitude,
        location.longitude
    )

    forecast = await WeatherService.get_forecast_for_date_range(
        location.latitude,
        location.longitude,
        start_date,
        end_date
    )

    hourly_forecast = await WeatherService.get_hourly_forecast(
        location.latitude,
        location.longitude
    )
    
    tips = generate_travel_tips(current_weather, forecast)

    db_request.location_query = location_query.strip()
    db_request.resolved_location = f"{location.city}, {location.country}"
    db_request.latitude = location.latitude
    db_request.longitude = location.longitude
    db_request.start_date = start_date
    db_request.end_date = end_date
    db_request.current_weather = json.dumps(current_weather.model_dump())
    db_request.forecast_data = json.dumps([day.model_dump() for day in forecast])
    db_request.hourly_forecast = json.dumps(hourly_forecast)
    db_request.travel_tips = json.dumps(tips)

    db.commit()
    db.refresh(db_request)

    return db_request


def delete_weather_request(db: Session, request_id: int):
    db_request = get_weather_request(db, request_id)

    db.delete(db_request)
    db.commit()

    return {
        "message": "Weather request deleted successfully",
        "deleted_id": request_id
    }