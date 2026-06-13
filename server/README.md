# Weather Travel Assistant - Backend

A robust FastAPI backend for real-time weather data, location management, and data export functionality.

## Features

✅ **Weather API Integration**
- Real-time weather data (Open-Meteo API - free, no API key required)
- 5-day forecast data
- Multiple weather parameters (temperature, humidity, wind speed, pressure, etc.)

✅ **Geocoding Services**
- Convert location names to coordinates
- Convert coordinates to location names
- Support for multiple location formats

✅ **CRUD Operations**
- Create saved weather requests
- Read weather history
- Update saved location information
- Delete saved locations
- Row-level operations with validation

✅ **Data Persistence**
- SQLite database (SQLAlchemy ORM)
- Automatic timestamps
- Data integrity with constraints

✅ **Data Export**
- JSON format
- CSV format
- Markdown format
- Streaming file responses

✅ **API Features**
- RESTful architecture
- CORS support
- Input validation (Pydantic)
- Error handling
- Health check endpoint
- Interactive API documentation (Swagger UI)

## Tech Stack

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Httpx** - Async HTTP client
- **SQLite** - Database

## Installation

1. **Create Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

   The server will start at `http://localhost:8000`

## API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Weather Endpoints

#### Get Current Weather
```
GET /api/weather/current
Query Parameters:
  - latitude (float, required): Latitude
  - longitude (float, required): Longitude

Response:
{
  "temperature": 22.5,
  "humidity": 65,
  "wind_speed": 12.3,
  "description": "Clear",
  "icon": "0",
  "feels_like": 21.0,
  "pressure": 1013,
  "visibility": 10000
}
```

#### Get 5-Day Forecast
```
GET /api/weather/forecast
Query Parameters:
  - latitude (float, required)
  - longitude (float, required)

Response:
{
  "forecast": [
    {
      "date": "2024-01-15",
      "temperature_max": 25.0,
      "temperature_min": 18.5,
      "description": "Partly Cloudy",
      "icon": "1",
      "precipitation_probability": 20
    }
  ]
}
```

### Geocoding Endpoints

#### Geocode Location
```
GET /api/geocode
Query Parameters:
  - location (string, required): Location name, ZIP code, or coordinates

Response:
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "United States"
}
```

#### Reverse Geocode
```
GET /api/reverse-geocode
Query Parameters:
  - latitude (float, required)
  - longitude (float, required)

Response:
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "United States"
}
```

### Saved Locations (CRUD)

#### List All Locations
```
GET /api/locations

Response:
[
  {
    "id": 1,
    "location": "New York, United States",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "temperature": 22.5,
    "description": "Clear",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

#### Create Location
```
POST /api/locations
Body:
{
  "location": "New York, United States",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "temperature": 22.5,
  "description": "Clear"
}

Response: [Location object]
```

#### Get Single Location
```
GET /api/locations/{location_id}

Response: [Location object]
```

#### Update Location
```
PUT /api/locations/{location_id}
Body:
{
  "location": "New York, NY",
  "description": "Partly Cloudy"
}

Response: [Updated location object]
```

#### Delete Location
```
DELETE /api/locations/{location_id}

Response:
{
  "message": "Location deleted successfully"
}
```

### Export Endpoints

#### Export Data
```
GET /api/export
Query Parameters:
  - format (string, required): "json", "csv", or "markdown"

Response: File download
```

### Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Project Structure

```
weather trends/
├── main.py              # FastAPI application and routes
├── config.py            # Configuration settings
├── database.py          # Database connection and initialization
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic request/response schemas
├── services.py          # Weather and geocoding services
├── export_service.py    # Data export functionality
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Database Schema

### SavedLocation Table
```sql
CREATE TABLE saved_locations (
  id INTEGER PRIMARY KEY,
  location VARCHAR(255) NOT NULL,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  temperature FLOAT NOT NULL,
  description VARCHAR(255) NOT NULL,
  icon VARCHAR(50),
  weather_data TEXT,
  created_at DATETIME,
  updated_at DATETIME
)
```

## Error Handling

The API provides consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- **200** - Success
- **400** - Bad request (validation error, invalid location)
- **404** - Resource not found
- **500** - Server error

## Validation

Using Pydantic for request validation:

- Location name: Required, string
- Latitude/Longitude: Required, float, range -90 to 90 / -180 to 180
- Temperature: Required, float
- Description: Required, string

## Security Considerations

- CORS enabled for frontend communication
- Input validation on all endpoints
- SQL injection protection (SQLAlchemy)
- Error messages don't expose sensitive info

## Environment Variables

Create a `.env` file (optional):

```env
DATABASE_URL=sqlite:///weather_app.db
DEBUG=False
HOST=0.0.0.0
PORT=8000
GOOGLE_MAPS_API_KEY=your_key_here
```

## Performance

- Async/await for non-blocking I/O
- Connection pooling
- Query optimization
- Efficient JSON serialization

## External APIs Used

1. **Open-Meteo Weather API**
   - Free, no API key required
   - Endpoint: https://api.open-meteo.com
   - Current weather and forecasts

2. **Open-Meteo Geocoding API**
   - Free, no API key required
   - Endpoint: https://geocoding-api.open-meteo.com
   - Location name to coordinates and vice versa

## Development

### Running in Debug Mode
```bash
DEBUG=true python main.py
```

### Database Inspection
The SQLite database file (`weather_app.db`) is created automatically in the project directory. You can inspect it with any SQLite client.

### Testing the API
Use the interactive Swagger UI at `http://localhost:8000/docs` to test all endpoints.

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker Support
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Integration

The frontend connects via:
- Base URL: `http://localhost:8000/api`
- All requests include proper CORS headers
- Async responses for better performance

## Troubleshooting

### Port Already in Use
```bash
# Change port
PORT=8001 python main.py
```

### Database Lock Error
```bash
# Delete existing database to start fresh
rm weather_app.db
python main.py
```

### Slow API Responses
- Check your internet connection (external API calls)
- Verify database is on local disk (not network drive)
- Check CPU usage and available memory

## Future Enhancements

- User authentication
- Rate limiting
- Caching layer (Redis)
- Advanced filtering/searching
- Analytics dashboard
- Webhook notifications
- Historical data analysis

## Support & Contributing

For issues or suggestions, please create an issue in the GitHub repository.

---

Built with ❤️ for PM Accelerator AI Engineer Assessment
