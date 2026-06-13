import React from 'react'
import styles from './CurrentWeather.module.css'
import { WeatherData } from '../services/api'
import { getWeatherIcon, getWeatherDescription } from '../utils/weather'
import { FiHeart } from 'react-icons/fi'
import { FaHeart } from 'react-icons/fa'

interface CurrentWeatherProps {
  data: WeatherData | null
  location: string
  isSaved: boolean
  onSave: () => void
  isLoading: boolean
}

export const CurrentWeather: React.FC<CurrentWeatherProps> = ({
  data,
  location,
  isSaved,
  onSave,
  isLoading
}) => {
  if (!data) return null

  return (
    <div className={styles.currentWeather}>
      <div className={styles.header}>
        <div>
          <h2 className={styles.location}>{location}</h2>
          <p className={styles.lastUpdated}>Real-time weather data</p>
        </div>
        <button
          className={styles.saveButton}
          onClick={onSave}
          disabled={isLoading}
          title={isSaved ? 'Unsave location' : 'Save location'}
        >
          {isSaved ? <FaHeart /> : <FiHeart />}
        </button>
      </div>

      <div className={styles.mainWeather}>
        <div className={styles.iconSection}>
          {getWeatherIcon(data.icon, 120)}
        </div>
        <div className={styles.tempSection}>
          <div className={styles.temperature}>{Math.round(data.temperature)}°C</div>
          <div className={styles.description}>{getWeatherDescription(data.icon)}</div>
          <div className={styles.feelsLike}>Feels like {Math.round(data.feels_like)}°C</div>
        </div>
      </div>

      <div className={styles.details}>
        <div className={styles.detailCard}>
          <label>Humidity</label>
          <div className={styles.detailValue}>{data.humidity}%</div>
        </div>
        <div className={styles.detailCard}>
          <label>Wind Speed</label>
          <div className={styles.detailValue}>{Math.round(data.wind_speed)} km/h</div>
        </div>
        <div className={styles.detailCard}>
          <label>Pressure</label>
          <div className={styles.detailValue}>{data.pressure} mb</div>
        </div>
        <div className={styles.detailCard}>
          <label>Visibility</label>
          <div className={styles.detailValue}>{(data.visibility / 1000).toFixed(1)} km</div>
        </div>
      </div>
    </div>
  )
}
