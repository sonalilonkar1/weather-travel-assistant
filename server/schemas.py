from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import date, datetime, timedelta
from typing import Any, List, Optional

FORECAST_RANGE_MESSAGE = (
    "Detailed forecasts are available for the next 5 days. "
    "For longer-term travel planning, please check closer to your trip date."
)

# Current weather data
class WeatherData(BaseModel):
    temperature: float
    humidity: int
    wind_speed: float
    description: str
    icon: str
    feels_like: float
    pressure: int
    visibility: float

# Daily forecast data
class ForecastDay(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    description: str
    icon: str
    precipitation_probability: int
    
# Hourly forecast data
class HourlyForecast(BaseModel):
    time: str
    temperature: float
    weather_code: str
    description: str
    precipitation_probability: int
    wind_speed: float

# Location information
class LocationData(BaseModel):
    latitude: float
    longitude: float
    city: str
    country: str

# Request to save a location
class SavedLocationCreate(BaseModel):
    location: str
    latitude: float
    longitude: float
    temperature: float
    description: str
    icon: Optional[str] = "0"

# Request to update a saved location
class SavedLocationUpdate(BaseModel):
    location: Optional[str] = None
    temperature: Optional[float] = None
    description: Optional[str] = None

# Response with saved location
class SavedLocationResponse(BaseModel):
    id: int
    location: str
    latitude: float
    longitude: float
    temperature: float
    description: str
    icon: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Request to create a weather request
class WeatherRequestCreate(BaseModel):
    location_query: str = Field(..., min_length=1, max_length=200)
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_date_range(self):
        today = date.today()
        max_forecast_date = today + timedelta(days=4)

        if (
            self.start_date < today
            or self.end_date > max_forecast_date
            or self.end_date < self.start_date
        ):
            raise ValueError(FORECAST_RANGE_MESSAGE)

        total_days = (self.end_date - self.start_date).days + 1

        if total_days > 5:
            raise ValueError(FORECAST_RANGE_MESSAGE)

        return self

# Request to update a weather request
class WeatherRequestUpdate(BaseModel):
    location_query: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    @field_validator("end_date")
    @classmethod
    def validate_update_date_range(cls, end_date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date and end_date < start_date:
            raise ValueError("end_date cannot be before start_date")
        return end_date
        
# Response with weather request details
class WeatherRequestResponse(BaseModel):
    id: int
    location_query: str
    resolved_location: str
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    current_weather: Any
    forecast_data: Any
    hourly_forecast: Any
    travel_tips: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# YouTube video data model
class YouTubeVideo(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail_url: str
    channel_title: str
    published_at: str
    video_url: str
    embed_url: str
    
# Error response model
class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
