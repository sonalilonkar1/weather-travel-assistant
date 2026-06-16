# Full-Stack Weather Travel Assistant

Search any location and plan ahead with live weather, hourly forecasts, advisories, saved history, and exportable reports.

## Author

Sonali Lonkar  
AI Engineer Intern Technical Assessment  
Completed: Full Stack Engineer - Tech Assignment #1 and Tech Assignment #2

## Project Overview

The Full-Stack Weather Travel Assistant is a web application that helps users check current and short-term weather conditions for a travel destination. Users can search by city, ZIP code, landmark, coordinates, or current browser location. The app displays current weather, hourly forecast, a 5-day forecast, weather advisories, travel tips, saved request history, and export options.

The project demonstrates full-stack development using a React frontend, a FastAPI backend, SQLite database persistence, external API integration, CRUD operations, validation, error handling, and data export.

## About Product Manager Accelerator

## PM Accelerator Mission
By making industry-leading tools and education available to individuals from all backgrounds, we level the playing field for future PM leaders. This is the PM Accelerator motto, as we grant aspiring and experienced PMs what they need most – Access. 
We introduce you to industry leaders, surround you with the right PM ecosystem, and discover the new world of AI product management skills.

More info on: `https://www.pmaccelerator.io/about-us` and `https://www.linkedin.com/school/pmaccelerator/`

## Features

### Frontend Features - Tech Assignment #1

- Search weather by city, ZIP code, landmark, or coordinates
- Use browser geolocation to get weather for the current location
- Display current weather conditions
- Display hourly forecast
- Display a 5-day forecast
- Show weather icons and condition descriptions
- Show weather advisories and travel tips
- Validate date ranges before making requests
- Show user-friendly error messages
- Responsive layout for desktop, tablet, and mobile
- Optional Google Maps location view
- Optional YouTube destination videos

### Backend Features - Tech Assignment #2

- FastAPI REST API backend
- SQLite database persistence with SQLAlchemy
- CRUD operations for saved weather requests
- Pydantic request and response validation
- Location validation and geocoding
- Date-range validation for supported forecast dates
- Open-Meteo weather and geocoding integration
- JSON export for saved weather requests
- CSV export for saved weather requests
- PDF export for saved weather requests
- Optional YouTube Data API integration for destination videos
- Clean error handling for invalid locations, unsupported dates, and API failures

## Supported Forecast Range

The app supports detailed forecasts for the next 5 days.

If a user selects a date outside the supported forecast window, the app shows:

```txt
Detailed forecasts are available for the next 5 days. For longer-term travel planning, please check closer to your trip date.
```

This keeps the app aligned with the assignment requirement and avoids showing unreliable long-range forecast data.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, TypeScript |
| Styling | CSS Modules |
| Backend | Python, FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| HTTP Client | Axios, httpx |
| Weather API | Open-Meteo API |
| Geocoding | Open-Meteo Geocoding API |
| Export | JSON, CSV, PDF |
| Optional Video API | YouTube Data API v3 |
| Optional Map API | Google Maps Embed API |

## Why Open-Meteo Was Used

Open-Meteo was selected because it provides current, hourly, and daily forecast data through a simple JSON API. It does not require an API key for basic non-commercial weather usage, which makes it easier to focus on the full-stack requirements of the assessment.

OpenWeatherMap and Weather Underground are also valid weather providers, but Open-Meteo reduced setup complexity and allowed the project to focus on frontend behavior, backend API design, database persistence, validation, and export functionality.

## Project Structure

```txt
weather app/
├── client/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CurrentWeather.tsx
│   │   │   ├── Forecast.tsx
│   │   │   ├── HourlyForecast.tsx
│   │   │   ├── WeatherAdvisory.tsx
│   │   │   ├── WeatherRequestHistory.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── ErrorMessage.tsx
│   │   │   ├── MapView.tsx
│   │   │   └── LocationVideos.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── utils/
│   │   │   └── weather.tsx
│   │   ├── App.tsx
│   │   ├── App.module.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
└── server/
    ├── main.py
    ├── models.py
    ├── schemas.py
    ├── database.py
    ├── services.py
    ├── crud.py
    ├── travel_tips.py
    ├── export_service.py
    ├── config.py
    └── requirements.txt
```

## Application Architecture

```txt
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  |-- Open-Meteo Weather API
  |-- Open-Meteo Geocoding API
  |-- YouTube Data API v3 - optional
  |-- Google Maps Embed API - optional frontend feature
  |
  v
SQLite Database
```

## Main User Flow

```txt
1. User enters a location and date range.
2. Frontend validates the input.
3. Frontend sends a POST request to the FastAPI backend.
4. Backend validates the request with Pydantic.
5. Backend geocodes the location into latitude and longitude.
6. Backend fetches current, hourly, and daily weather data from Open-Meteo.
7. Backend generates advisories and travel tips.
8. Backend saves the weather request and result in SQLite.
9. Backend returns the saved result to the frontend.
10. Frontend displays current weather, hourly forecast, 5-day forecast, advisories, tips, and history.
```

## Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check endpoint |
| POST | `/api/weather-requests` | Create a new weather request |
| GET | `/api/weather-requests` | Get all saved weather requests |
| GET | `/api/weather-requests/{id}` | Get one saved weather request |
| PUT | `/api/weather-requests/{id}` | Update a saved weather request |
| DELETE | `/api/weather-requests/{id}` | Delete a saved weather request |
| GET | `/api/weather-requests/export?format=json` | Export saved requests as JSON |
| GET | `/api/weather-requests/export?format=csv` | Export saved requests as CSV |
| GET | `/api/weather-requests/export?format=pdf` | Export saved requests as PDF |
| GET | `/api/videos?location=LOCATION` | Optional: get YouTube videos for a location |

FastAPI interactive API documentation is available at:

```txt
http://localhost:8000/docs
```

## Database Model

The main saved entity is a weather request.

Each saved weather request stores:

- Original location query
- Resolved location name
- Latitude and longitude
- Start date and end date
- Current weather data
- Hourly forecast data
- 5-day forecast data
- Weather advisories and travel tips
- Created and updated timestamps

Nested weather data is stored as JSON text in SQLite and converted back into structured JSON responses for the frontend.

## Environment Variables

Create environment files locally. Do not commit real API keys.

### Frontend: `client/.env`

```env
VITE_API_URL=http://localhost:8000/api
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

`VITE_GOOGLE_MAPS_API_KEY` is optional. If it is not provided, the map feature can be hidden.

### Backend: `server/.env`

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

`YOUTUBE_API_KEY` is optional. If it is not provided, the app can still run without YouTube destination videos.

## Setup Instructions

### Prerequisites

- Node.js 18 or newer
- Python 3.11 recommended
- npm
- Git

### 1. Clone the Repository

```bash
git clone REPOSITORY_URL
cd "weather app"
```

### 2. Start the Backend

```bash
cd server
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend runs at:

```txt
http://localhost:8000
```

### 3. Start the Frontend

Open a new terminal:

```bash
cd client
npm install
npm run dev
```

Frontend runs at:

```txt
http://localhost:5173
```

## Build Check

```bash
cd client
npm run build
```

The frontend build should complete successfully without TypeScript errors.

## Export Options

Saved weather requests can be exported in three formats:

- JSON - structured data for developers or backup
- CSV - spreadsheet-friendly format
- PDF - readable weather report format

PDF export includes a report-style summary of saved weather requests, current conditions, advisories, travel tips, and 5-day forecast data.

## Error Handling

The app handles common error cases, including:

- Empty location input
- Invalid location
- Unsupported date range
- End date before start date
- Geolocation permission denied
- External API failures
- Export failures

Invalid long-range forecast message:

```txt
Detailed forecasts are available for the next 5 days. For longer-term travel planning, please check closer to your trip date.
```

## Demo Video

Demo Video URL: DEMO_VIDEO_URL

## GitHub Repository

Repository URL: GITHUB_REPOSITORY_URL

## Notes

This project is built for technical assessment and learning purposes. It demonstrates frontend development, backend API design, external API integration, validation, persistence, CRUD operations, and export functionality.

## License

This project is open source and available for evaluation purposes.