from typing import List
from schemas import WeatherData, ForecastDay


def generate_travel_tips(
    current_weather: WeatherData,
    forecast: List[ForecastDay]
) -> List[str]:
    tips = []

    if current_weather.temperature >= 30:
        tips.append("Heat Advisory: High temperatures expected. Stay hydrated and avoid long exposure to direct sun.")
        tips.append("Carry water and avoid strenuous outdoor activity during peak afternoon hours.")

    if current_weather.temperature <= 0:
        tips.append("Freeze Advisory: Temperatures are near or below freezing. Dress warmly and watch for icy surfaces.")

    if current_weather.wind_speed >= 35:
        tips.append("Wind Advisory: Strong winds may affect driving, biking, or outdoor activities.")

    rainy_days = [
        day for day in forecast
        if day.precipitation_probability >= 60
    ]

    if rainy_days:
        tips.append("Rain Advisory: Rain is likely during this date range. Bring an umbrella or rain jacket.")

    snow_days = [
        day for day in forecast
        if "snow" in day.description.lower()
    ]

    if snow_days:
        tips.append("Snow Advisory: Snow is possible. Check road conditions and dress for winter weather.")

    large_temperature_swings = [
        day for day in forecast
        if abs(day.temperature_max - day.temperature_min) >= 12
    ]

    if large_temperature_swings:
        tips.append("Dress in layers because temperatures may change significantly throughout the day.")

    if not tips:
        tips.append("No major weather advisories. Conditions look comfortable for most plans.")

    return tips