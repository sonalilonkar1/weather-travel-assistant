from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

# Model for saving weather searches
class SavedLocation(Base):
    __tablename__ = "saved_locations"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(50), default="0")
    weather_data = Column(Text)  # Store full JSON weather data
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True


# Model for storing weather requests and results
class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    location_query = Column(String(255), nullable=False)
    resolved_location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    hourly_forecast = Column(Text, nullable=True)
    

    current_weather = Column(Text, nullable=False)
    forecast_data = Column(Text, nullable=False)
    travel_tips = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())