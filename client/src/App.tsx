import { useEffect, useState } from 'react'
import styles from './App.module.css'

import { SearchBar } from './components/SearchBar'
import { CurrentWeather } from './components/CurrentWeather'
import { Forecast } from './components/Forecast'
import { MapView } from './components/MapView'
import { ErrorMessage } from './components/ErrorMessage'
import WeatherRequestHistory from './components/WeatherRequestHistory'
import HourlyForecast from './components/HourlyForecast'
import WeatherAdvisory from './components/WeatherAdvisory'
import { HourlyForecast as HourlyForecastType } from './services/api'
import LocationVideos from './components/LocationVideos'

import {
  WeatherData,
  ForecastData,
  WeatherRequest,
  createWeatherRequest,
  getWeatherRequests,
  deleteWeatherRequest,
  exportWeatherRequests,
  handleError
} from './services/api'

import { downloadFile } from './utils/weather'

function App() {
  const [currentWeather, setCurrentWeather] = useState<WeatherData | null>(null)
  const [forecast, setForecast] = useState<ForecastData[] | null>(null)
  const [hourlyForecast, setHourlyForecast] = useState<HourlyForecastType[] | null>(null)

  const [currentLocation, setCurrentLocation] = useState('')
  const [currentCoords, setCurrentCoords] = useState<{ lat: number; lon: number } | null>(null)

  const [weatherRequests, setWeatherRequests] = useState<WeatherRequest[]>([])
  const [selectedRequest, setSelectedRequest] = useState<WeatherRequest | null>(null)

  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadWeatherRequests()
  }, [])

  const loadWeatherRequests = async () => {
    try {
      const requests = await getWeatherRequests()
      setWeatherRequests(requests)
    } catch {
      console.log('Could not load weather request history. Backend may not be ready.')
      setWeatherRequests([])
    }
  }

  const applyWeatherRequestToScreen = (request: WeatherRequest) => {
    setSelectedRequest(request)
    setCurrentWeather(request.current_weather)
    setForecast(request.forecast_data)
    setHourlyForecast(request.hourly_forecast)
    setCurrentLocation(request.resolved_location)
    setCurrentCoords({
      lat: request.latitude,
      lon: request.longitude
    })
  }

  const clearWeatherScreen = () => {
    setCurrentWeather(null)
    setForecast(null)
    setHourlyForecast(null)
    setCurrentCoords(null)
    setSelectedRequest(null)
  }

  const handleSearch = async (
    location: string,
    startDate: string,
    endDate: string
  ) => {
    setIsLoading(true)
    setError('')

    try {
      const request = await createWeatherRequest(location, startDate, endDate)
      applyWeatherRequestToScreen(request)
      await loadWeatherRequests()
    } catch (err) {
      setError(handleError(err))
      clearWeatherScreen()
    } finally {
      setIsLoading(false)
    }
  }

  const handleCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.')
      return
    }

    setIsLoading(true)
    setError('')

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords

        const today = new Date()
        const end = new Date()
        end.setDate(today.getDate() + 4)

        const startDate = today.toISOString().split('T')[0]
        const endDate = end.toISOString().split('T')[0]

        await handleSearch(`${latitude}, ${longitude}`, startDate, endDate)
      },
      (geoError) => {
        setError(`Location permission error: ${geoError.message}`)
        setIsLoading(false)
      }
    )
  }

  const handleSelectRequest = (request: WeatherRequest) => {
    applyWeatherRequestToScreen(request)
  }

  const handleDeleteRequest = async (id: number) => {
    setIsLoading(true)
    setError('')

    try {
      await deleteWeatherRequest(id)
      await loadWeatherRequests()

      if (selectedRequest?.id === id) {
        setCurrentWeather(null)
        setForecast(null)
        setHourlyForecast(null)
        setCurrentLocation('')
        setCurrentCoords(null)
        setSelectedRequest(null)
      }
    } catch (err) {
      setError(handleError(err))
    } finally {
      setIsLoading(false)
    }
  }

  const handleExportRequests = async (format: 'json' | 'csv' | 'pdf') => {
    setIsLoading(true)
    setError('')

    try {
      const blob = await exportWeatherRequests(format)
      const today = new Date().toISOString().split('T')[0]
      downloadFile(blob, `weather-requests-${today}.${format}`)
    } catch (err) {
      setError(handleError(err))
    } finally {
      setIsLoading(false)
    }
  }

  const handleSaveAlreadyStoredRequest = () => {
    setError('This weather request is already saved in your request history.')
  }

  const allTips = selectedRequest?.travel_tips || []

  const advisoryKeywords = [
    'advisory',
    'warning',
    'alert',
    'heat',
    'snow',
    'rain',
    'wind',
    'freeze',
    'storm',
    'thunder',
    'icy',
    'flood'
  ]

  const advisoryTips = allTips.filter((tip) =>
    advisoryKeywords.some((keyword) =>
      tip.toLowerCase().includes(keyword)
    )
  )

  const practicalTips = allTips.filter((tip) => {
    const lowerTip = tip.toLowerCase()

    const isAdvisory = advisoryKeywords.some((keyword) =>
      lowerTip.includes(keyword)
    )

    return !isAdvisory
  })

  const isSaved = Boolean(selectedRequest)

  return (
    <div className={styles.app}>
      <div className={styles.container}>
        <header className={styles.header}>
          <div>
            <h1 className={styles.title}>🌤️ Weather Travel Assistant</h1>
            <p className={styles.subtitle}>
              Check current conditions, hourly changes, 5-day forecasts, and weather risks before you go.
            </p>
          </div>
        </header>

        {error && (
          <ErrorMessage
            message={error}
            onClose={() => setError('')}
            type="error"
          />
        )}

        <SearchBar
          onSearch={handleSearch}
          onCurrentLocation={handleCurrentLocation}
          isLoading={isLoading}
        />

        <CurrentWeather
          data={currentWeather}
          location={currentLocation}
          isSaved={isSaved}
          onSave={handleSaveAlreadyStoredRequest}
          isLoading={isLoading}
        />

        <WeatherAdvisory tips={advisoryTips} />

        <HourlyForecast data={hourlyForecast} />

        <Forecast data={forecast} />

        {practicalTips.length > 0 && (
          <section
            style={{
              background: 'rgba(255, 255, 255, 0.1)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              borderRadius: '16px',
              padding: '24px',
              marginBottom: '32px',
              color: 'white'
            }}
          >
            <h3 style={{ marginBottom: '12px' }}>Travel Tips</h3>
            <ul style={{ paddingLeft: '20px', lineHeight: 1.7 }}>
              {practicalTips.map((tip, index) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </section>
        )}

        {currentLocation && (
          <LocationVideos location={currentLocation} />
        )}

        {currentCoords && (
          <MapView
            latitude={currentCoords.lat}
            longitude={currentCoords.lon}
            city={currentLocation}
          />
        )}

        <WeatherRequestHistory
          requests={weatherRequests}
          onSelect={handleSelectRequest}
          onDelete={handleDeleteRequest}
          onExport={handleExportRequests}
          isLoading={isLoading}
        />

        <footer className={styles.footer}>
          <p>
            Built by Sonali Lonkar for the AI Engineer Intern Technical Assessment (Full Stack).
          </p>
          <p>
            Tech Stack: React, TypeScript, FastAPI, SQLite, Open-Meteo API
          </p>
          <p>
            <a
              href="https://www.linkedin.com/school/pmaccelerator/"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn more about PM Accelerator →
            </a>
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App