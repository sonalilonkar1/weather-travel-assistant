import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

export interface WeatherData {
  temperature: number
  humidity: number
  wind_speed: number
  description: string
  icon: string
  feels_like: number
  pressure: number
  visibility: number
}

export interface ForecastData {
  date: string
  temperature_max: number
  temperature_min: number
  description: string
  icon: string
  precipitation_probability: number
}

export interface ForecastDay {
  date: string
  temperature_max: number
  temperature_min: number
  description: string
  icon: string
  precipitation_probability: number
}

export interface LocationData {
  latitude: number
  longitude: number
  city: string
  country: string
}

export interface WeatherRequest {
  id: number
  location_query: string
  resolved_location: string
  latitude: number
  longitude: number
  start_date: string
  end_date: string
  current_weather: WeatherData
  forecast_data: ForecastData[]
  hourly_forecast: HourlyForecast[]
  travel_tips: string[]
  created_at: string
  updated_at: string
}

export interface SavedLocation {
  id: number
  location: string
  latitude: number
  longitude: number
  temperature: number
  description: string
  icon: string
  created_at: string
  updated_at: string
}

export interface HourlyForecast {
  time: string
  temperature: number
  weather_code: string
  description: string
  precipitation_probability: number
  wind_speed: number
}

export interface YouTubeVideo {
  video_id: string
  title: string
  description: string
  thumbnail_url: string
  channel_title: string
  published_at: string
  video_url: string
  embed_url: string
}

export const createWeatherRequest = async (
  locationQuery: string,
  startDate: string,
  endDate: string
): Promise<WeatherRequest> => {
  const response = await api.post('/weather-requests', {
    location_query: locationQuery,
    start_date: startDate,
    end_date: endDate
  })

  return response.data
}

export const getWeatherRequests = async (): Promise<WeatherRequest[]> => {
  const response = await api.get('/weather-requests')
  return response.data
}

export const getWeatherRequest = async (id: number): Promise<WeatherRequest> => {
  const response = await api.get(`/weather-requests/${id}`)
  return response.data
}

export const updateWeatherRequest = async (
  id: number,
  data: Partial<{
    location_query: string
    start_date: string
    end_date: string
  }>
): Promise<WeatherRequest> => {
  const response = await api.put(`/weather-requests/${id}`, data)
  return response.data
}

export const deleteWeatherRequest = async (id: number): Promise<void> => {
  await api.delete(`/weather-requests/${id}`)
}

export const exportWeatherRequests = async (
  format: 'json' | 'csv' | 'pdf'
): Promise<Blob> => {
  const response = await api.get('/weather-requests/export', {
    params: { format },
    responseType: 'blob'
  })

  return response.data
}

export const getCurrentWeather = async (
  latitude: number,
  longitude: number
): Promise<WeatherData> => {
  const response = await api.get('/weather/current', {
    params: { latitude, longitude }
  })

  return response.data
}

export const getForecast = async (
  latitude: number,
  longitude: number
): Promise<ForecastData[]> => {
  const response = await api.get('/weather/forecast', {
    params: { latitude, longitude }
  })

  return response.data.forecast
}

export const geocodeLocation = async (
  location: string
): Promise<LocationData> => {
  const response = await api.get('/geocode', {
    params: { location }
  })

  return response.data
}

export const reverseGeocode = async (
  latitude: number,
  longitude: number
): Promise<LocationData> => {
  const response = await api.get('/reverse-geocode', {
    params: { latitude, longitude }
  })

  return response.data
}

export const getLocationVideos = async (
  location: string
): Promise<YouTubeVideo[]> => {
  const response = await api.get('/videos', {
    params: { location }
  })

  return response.data
}

export const handleError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail

    if (typeof detail === 'string') {
      return detail
    }

    if (Array.isArray(detail)) {
      return detail.map((item) => item.msg).join(', ')
    }

    if (error.message) {
      return error.message
    }
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'Something went wrong. Please try again.'
}