import httpx
from typing import List
import logging
from schemas import WeatherData, ForecastDay, LocationData
from config import WEATHER_API, GEOCODING_API, YOUTUBE_API_KEY

logger = logging.getLogger(__name__)

# WMO Weather Code Mapping
# Reference: https://www.open-meteo.com/en/docs
WEATHER_CODES = {
    "0": "Clear",
    "1": "Partly Cloudy",
    "2": "Cloudy",
    "3": "Overcast",
    "45": "Foggy",
    "48": "Rime Fog",
    "51": "Light Drizzle",
    "53": "Moderate Drizzle",
    "55": "Heavy Drizzle",
    "61": "Slight Rain",
    "63": "Moderate Rain",
    "65": "Heavy Rain",
    "71": "Slight Snow",
    "73": "Moderate Snow",
    "75": "Heavy Snow",
    "77": "Snow Grains",
    "80": "Rain Showers",
    "81": "Heavy Rain Showers",
    "82": "Violent Rain Showers",
    "85": "Snow Showers",
    "86": "Heavy Snow Showers",
    "95": "Thunderstorm",
    "96": "Thunderstorm + Hail",
    "99": "Thunderstorm + Heavy Hail",
}

# Fetch weather data and generate travel tips based on conditions.
class WeatherService:
    # Timeout for external API calls (seconds)
    API_TIMEOUT = 10

    # Fetch current weather conditions for given coordinates
    @staticmethod
    async def get_current_weather(latitude: float, longitude: float) -> WeatherData:
        try:
            logger.debug(f"Fetching current weather for ({latitude}, {longitude})")
            
            async with httpx.AsyncClient(timeout=WeatherService.API_TIMEOUT) as client:
                response = await client.get(
                    f"{WEATHER_API}/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        # Request specific weather variables
                        "current": (
                            "temperature_2m,"
                            "relative_humidity_2m,"
                            "apparent_temperature,"
                            "weather_code,"
                            "wind_speed_10m,"
                            "pressure_msl,"
                            "visibility"
                        ),
                        "temperature_unit": "celsius"
                    }
                )
                response.raise_for_status()
                data = response.json()

                current = data.get("current", {})
                if not current:
                    raise ValueError("No current weather data in API response")
                
                weather_code = str(current.get("weather_code", 0))

                return WeatherData(
                    temperature=float(current.get("temperature_2m", 0)),
                    humidity=int(current.get("relative_humidity_2m", 0)),
                    wind_speed=float(current.get("wind_speed_10m", 0)),
                    description=WeatherService._get_weather_description(weather_code),
                    icon=weather_code,
                    feels_like=float(current.get("apparent_temperature", 0)),
                    pressure=int(current.get("pressure_msl", 0)),
                    visibility=float(current.get("visibility", 10000))
                )
                
        except httpx.TimeoutException as e:
            logger.error(f"Weather API timeout: {e}")
            raise Exception("Weather service is taking too long. Please try again.")
        except httpx.HTTPStatusError as e:
            logger.error(f"Weather API error {e.response.status_code}: {e}")
            raise Exception("Weather service temporarily unavailable.")
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")

    # Fetch hourly forecast for the next 24 hours starting from the current hour
    @staticmethod
    async def get_hourly_forecast(latitude: float, longitude: float):
        try:
            from datetime import datetime

            logger.debug(f"Fetching hourly forecast for ({latitude}, {longitude})")

            async with httpx.AsyncClient(timeout=WeatherService.API_TIMEOUT) as client:
                response = await client.get(
                    f"{WEATHER_API}/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": "temperature_2m",
                        "hourly": (
                            "temperature_2m,"
                            "weather_code,"
                            "precipitation_probability,"
                            "wind_speed_10m"
                        ),
                        "forecast_days": 2,
                        "temperature_unit": "celsius",
                        "wind_speed_unit": "kmh",
                        "timezone": "auto"
                    }
                )

                response.raise_for_status()
                data = response.json()

                hourly = data.get("hourly", {})
                times = hourly.get("time", [])
                temperatures = hourly.get("temperature_2m", [])
                weather_codes = hourly.get("weather_code", [])
                precipitation = hourly.get("precipitation_probability", [])
                wind_speeds = hourly.get("wind_speed_10m", [])

                current_time = data.get("current", {}).get("time")

                if current_time:
                    current_hour = current_time[:13]
                else:
                    current_hour = datetime.now().strftime("%Y-%m-%dT%H")

                start_index = 0

                for index, time_value in enumerate(times):
                    if time_value[:13] >= current_hour:
                        start_index = index
                        break

                logger.info(
                    f"Hourly forecast starts at index {start_index}, "
                    f"time={times[start_index] if times else 'N/A'}, "
                    f"current_hour={current_hour}"
                )

                results = []
                end_index = min(start_index + 24, len(times))

                for i in range(start_index, end_index):
                    code = str(weather_codes[i]) if i < len(weather_codes) else "0"

                    results.append({
                        "time": times[i],
                        "temperature": float(temperatures[i]) if i < len(temperatures) else 0,
                        "weather_code": code,
                        "description": WeatherService._get_weather_description(code),
                        "precipitation_probability": int(precipitation[i]) if i < len(precipitation) else 0,
                        "wind_speed": float(wind_speeds[i]) if i < len(wind_speeds) else 0
                    })

                return results

        except Exception as e:
            logger.error(f"Error fetching hourly forecast: {e}")
            raise Exception(f"Failed to fetch hourly forecast: {str(e)}")
    
    # Fetch 5-day forecast with daily high/low temps and conditions
    @staticmethod
    async def get_forecast(latitude: float, longitude: float) -> List[ForecastDay]:
        try:
            logger.debug(f"Fetching 5-day forecast for ({latitude}, {longitude})")
            
            async with httpx.AsyncClient(timeout=WeatherService.API_TIMEOUT) as client:
                response = await client.get(
                    f"{WEATHER_API}/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": (
                            "weather_code,"
                            "temperature_2m_max,"
                            "temperature_2m_min,"
                            "precipitation_probability_max"
                        ),
                        "temperature_unit": "celsius",
                        "timezone": "auto",
                        "forecast_days": 5
                    }
                )
                response.raise_for_status()
                data = response.json()

                forecast_list = []
                daily = data.get("daily", {})
                
                if not daily:
                    logger.warning("No daily forecast data in API response")
                    return forecast_list

                dates = daily.get("time", [])
                weather_codes = daily.get("weather_code", [])
                temp_max = daily.get("temperature_2m_max", [])
                temp_min = daily.get("temperature_2m_min", [])
                precip_prob = daily.get("precipitation_probability_max", [])

                # Build forecast list
                for i in range(min(len(dates), 5)):  # Max 5 days
                    weather_code = str(weather_codes[i]) if i < len(weather_codes) else "0"
                    
                    forecast_list.append(
                        ForecastDay(
                            date=dates[i],
                            temperature_max=float(temp_max[i]) if i < len(temp_max) else 0,
                            temperature_min=float(temp_min[i]) if i < len(temp_min) else 0,
                            description=WeatherService._get_weather_description(weather_code),
                            icon=weather_code,
                            precipitation_probability=int(precip_prob[i]) if i < len(precip_prob) else 0
                        )
                    )

                logger.info(f"Successfully fetched {len(forecast_list)} days of forecast")
                return forecast_list
                
        except httpx.TimeoutException as e:
            logger.error(f"Forecast API timeout: {e}")
            raise Exception("Forecast service is taking too long. Please try again.")
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            raise Exception(f"Failed to fetch forecast: {str(e)}")

    # Fetch forecast for a specific date range (used by backend CRUD requirement)
    @staticmethod
    async def get_forecast_for_date_range(
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ) -> List[ForecastDay]:
        try:
            logger.debug(
                f"Fetching forecast for ({latitude}, {longitude}) "
                f"from {start_date} to {end_date}"
            )

            async with httpx.AsyncClient(timeout=WeatherService.API_TIMEOUT) as client:
                response = await client.get(
                    f"{WEATHER_API}/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "daily": (
                            "weather_code,"
                            "temperature_2m_max,"
                            "temperature_2m_min,"
                            "precipitation_probability_max,"
                            "wind_speed_10m_max"
                        ),
                        "temperature_unit": "celsius",
                        "timezone": "auto",
                        "start_date": start_date,
                        "end_date": end_date
                    }
                )

                response.raise_for_status()
                data = response.json()

                daily = data.get("daily", {})
                dates = daily.get("time", [])
                weather_codes = daily.get("weather_code", [])
                temp_max = daily.get("temperature_2m_max", [])
                temp_min = daily.get("temperature_2m_min", [])
                precip_prob = daily.get("precipitation_probability_max", [])

                forecast_list = []

                for i in range(len(dates)):
                    weather_code = str(weather_codes[i]) if i < len(weather_codes) else "0"

                    forecast_list.append(
                        ForecastDay(
                            date=dates[i],
                            temperature_max=float(temp_max[i]) if i < len(temp_max) else 0,
                            temperature_min=float(temp_min[i]) if i < len(temp_min) else 0,
                            description=WeatherService._get_weather_description(weather_code),
                            icon=weather_code,
                            precipitation_probability=int(precip_prob[i]) if i < len(precip_prob) else 0
                        )
                    )

                return forecast_list

        except httpx.TimeoutException:
            logger.error("Date-range forecast API timeout")
            raise Exception("Forecast service is taking too long. Please try again.")
        except Exception as e:
            logger.error(f"Error fetching date-range forecast: {e}")
            raise Exception(f"Failed to fetch forecast for date range: {str(e)}")
    
    # Helper method to convert WMO weather code to description
    @staticmethod
    def _get_weather_description(code: str) -> str:
       return WEATHER_CODES.get(code, "Unknown")

# Convert location names or coordinates to a standardized format using Open-Meteo geocoding API.
class GeocodingService:
    API_TIMEOUT = 10

    # Convert location name/ZIP/coordinates to coordinates.
    @staticmethod
    async def geocode_location(location: str) -> LocationData:
        try:
            logger.debug(f"Geocoding location: {location}")
            
            # Try to parse as coordinates first, for example "37.3382, -121.8863"
            parts = location.replace(",", " ").strip().split()

            if len(parts) == 2:
                try:
                    lat = float(parts[0])
                    lon = float(parts[1])

                    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                        raise ValueError("Coordinates out of range")

                    logger.debug(f"Parsed coordinates directly: {lat}, {lon}")

                    return await GeocodingService.reverse_geocode(lat, lon)

                except ValueError:
                    # Not valid coordinates, continue to normal location search
                    pass

            # Search by location name (city, ZIP code, landmark, etc)
            async with httpx.AsyncClient(timeout=GeocodingService.API_TIMEOUT) as client:
                response = await client.get(
                    f"{GEOCODING_API}/v1/search",
                    params={
                        "name": location.strip(),
                        "count": 1,  # Get best match only
                        "language": "en",
                        "format": "json"
                    }
                )
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                if not results:
                    logger.warning(f"No results found for: {location}")
                    raise Exception(f"'{location}' not found. Try another search.")

                result = results[0]
                location_data = LocationData(
                    latitude=float(result.get("latitude", 0)),
                    longitude=float(result.get("longitude", 0)),
                    city=result.get("name", "Unknown"),
                    country=result.get("country", "Unknown")
                )
                
                logger.info(f"Found: {location_data.city}, {location_data.country}")
                return location_data
                
        except httpx.TimeoutException:
            logger.error("Geocoding API timeout")
            raise Exception("Geocoding service is slow. Please try again.")
        except httpx.HTTPStatusError as e:
            logger.error(f"Geocoding API error: {e}")
            raise Exception("Geocoding service unavailable. Try again later.")
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            raise

    # Convert coordinates to a readable location name.
    @staticmethod
    async def reverse_geocode(latitude: float, longitude: float) -> LocationData:
        try:
            logger.debug(f"Reverse geocoding: {latitude}, {longitude}")

            async with httpx.AsyncClient(timeout=GeocodingService.API_TIMEOUT) as client:
                response = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                        "zoom": 10,
                        "addressdetails": 1
                    },
                    headers={
                        "User-Agent": "WeatherTravelAssistant/1.0"
                    }
                )

                response.raise_for_status()
                data = response.json()

                address = data.get("address", {})

                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("village")
                    or address.get("municipality")
                    or address.get("county")
                    or "Current Location"
                )

                state = address.get("state")
                country = address.get("country", "")

                if state and country:
                    country_display = f"{state}, {country}"
                else:
                    country_display = country or f"{latitude:.4f}, {longitude:.4f}"

                return LocationData(
                    latitude=latitude,
                    longitude=longitude,
                    city=city,
                    country=country_display
                )

        except Exception as e:
            logger.error(f"Reverse geocoding error: {e}")

            return LocationData(
                latitude=latitude,
                longitude=longitude,
                city="Current Location",
                country=f"{latitude:.4f}, {longitude:.4f}"
            )

# Service for fetching YouTube videos related to a travel location.       
class YouTubeService:

    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    # Search for travel guide videos related to the location.
    @staticmethod
    async def search_location_videos(location: str, max_results: int = 3):
        if not YOUTUBE_API_KEY:
            logger.warning("YouTube API key is not configured.")
            return []

        search_query = f"{location} travel guide things to do"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                YouTubeService.BASE_URL,
                params={
                    "part": "snippet",
                    "q": search_query,
                    "type": "video",
                    "maxResults": max_results,
                    "safeSearch": "moderate",
                    "videoEmbeddable": "true",
                    "key": YOUTUBE_API_KEY,
                },
            )

            response.raise_for_status()
            data = response.json()

        videos = []

        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})

            if not video_id:
                continue

            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "description": snippet.get("description", ""),
                "thumbnail_url": snippet.get("thumbnails", {})
                    .get("medium", {})
                    .get("url", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "published_at": snippet.get("publishedAt", ""),
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "embed_url": f"https://www.youtube.com/embed/{video_id}",
            })

        return videos
