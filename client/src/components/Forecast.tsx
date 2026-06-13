import React from 'react'
import styles from './Forecast.module.css'
import { ForecastData } from '../services/api'
import { getWeatherIcon, formatDate } from '../utils/weather'

interface ForecastProps {
  data: ForecastData[] | null
}

export const Forecast: React.FC<ForecastProps> = ({ data }) => {
  if (!data || data.length === 0) return null

  return (
    <div className={styles.forecast}>
      <h3 className={styles.title}>5-Day Forecast</h3>
      <div className={styles.forecastGrid}>
        {data.map((day, index) => (
          <div key={index} className={styles.forecastCard}>
            <div className={styles.date}>{formatDate(day.date)}</div>
            <div className={styles.icon}>{getWeatherIcon(day.icon, 48)}</div>
            <div className={styles.temps}>
              <span className={styles.maxTemp}>{Math.round(day.temperature_max)}°</span>
              <span className={styles.minTemp}>{Math.round(day.temperature_min)}°</span>
            </div>
            <div className={styles.description}>{day.description}</div>
            <div className={styles.precipitation}>
              💧 {day.precipitation_probability}%
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
