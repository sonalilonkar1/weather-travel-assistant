import { useRef } from 'react'
import { FiChevronLeft, FiChevronRight } from 'react-icons/fi'
import { HourlyForecast as HourlyForecastType } from '../services/api'
import { getWeatherIcon } from '../utils/weather'
import styles from './HourlyForecast.module.css'

interface HourlyForecastProps {
  data: HourlyForecastType[] | null
}

function formatHour(time: string, index: number) {
  if (index === 0) {
    return 'Now'
  }

  const date = new Date(time)
  return date.toLocaleTimeString([], {
    hour: 'numeric',
    hour12: true
  })
}

export default function HourlyForecast({ data }: HourlyForecastProps) {
  const scrollerRef = useRef<HTMLDivElement | null>(null)

  if (!data || data.length === 0) {
    return null
  }

  const scrollLeft = () => {
    scrollerRef.current?.scrollBy({
      left: -360,
      behavior: 'smooth'
    })
  }

  const scrollRight = () => {
    scrollerRef.current?.scrollBy({
      left: 360,
      behavior: 'smooth'
    })
  }

  return (
    <section className={styles.hourlyCard}>
      <div className={styles.header}>
        <p className={styles.summary}>
          Hourly forecast for the next 24 hours
        </p>

        <div className={styles.arrowButtons}>
          <button
            type="button"
            className={styles.arrowButton}
            onClick={scrollLeft}
            aria-label="Scroll hourly forecast left"
          >
            <FiChevronLeft />
          </button>

          <button
            type="button"
            className={styles.arrowButton}
            onClick={scrollRight}
            aria-label="Scroll hourly forecast right"
          >
            <FiChevronRight />
          </button>
        </div>
      </div>

      <div className={styles.hourlyWrapper}>
        <div ref={scrollerRef} className={styles.hourlyScroller}>
          {data.slice(0, 24).map((hour, index) => (
            <div key={hour.time} className={styles.hourCard}>
              <span className={styles.hour}>
                {formatHour(hour.time, index)}
              </span>

              <div className={styles.icon}>
                {getWeatherIcon(hour.weather_code, 34)}
              </div>

              <span className={styles.temp}>
                {Math.round(hour.temperature)}°
              </span>

              {hour.precipitation_probability > 20 && (
                <span className={styles.rain}>
                  {hour.precipitation_probability}%
                </span>
              )}
            </div>
          ))}
        </div>

        <button
          type="button"
          className={styles.floatingArrow}
          onClick={scrollRight}
          aria-label="See more hourly forecast"
        >
          <FiChevronRight />
        </button>
      </div>
    </section>
  )
}