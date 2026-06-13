import { useState } from 'react'
import type { FormEvent } from 'react'
import { FiMapPin, FiSearch } from 'react-icons/fi'
import styles from './SearchBar.module.css'

export interface SearchBarProps {
  onSearch: (location: string, startDate: string, endDate: string) => void
  onCurrentLocation: () => void
  isLoading: boolean
}

function getTodayDate() {
  return new Date().toISOString().split('T')[0]
}

function getDefaultEndDate() {
  const date = new Date()
  date.setDate(date.getDate() + 4)
  return date.toISOString().split('T')[0]
}

const FORECAST_RANGE_MESSAGE =
  'Detailed forecasts are available for the next 5 days. For longer-term travel planning, please check closer to your trip date.'

const getLocalDateString = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const addDays = (dateString: string, days: number) => {
  const date = new Date(`${dateString}T00:00:00`)
  date.setDate(date.getDate() + days)

  return getLocalDateString(date)
}

const parseLocalDate = (dateString: string) => {
  return new Date(`${dateString}T00:00:00`)
}

export const SearchBar = ({
  onSearch,
  onCurrentLocation,
  isLoading
}: SearchBarProps) => {
  const today = getLocalDateString(new Date())
  const maxForecastDate = addDays(today, 4)

  const [error, setError] = useState('')
  const [location, setLocation] = useState('')
  const [startDate, setStartDate] = useState(getTodayDate())
  const [endDate, setEndDate] = useState(getDefaultEndDate())
  const [localError, setLocalError] = useState('')

  const isDateRangeInvalid = Boolean(
    startDate && endDate && new Date(startDate) > new Date(endDate)
  )

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLocalError('')

    const trimmedLocation = location.trim()

    if (!trimmedLocation) {
      setLocalError('Please enter a city, ZIP code, landmark, or coordinates.')
      return
    }

    if (isDateRangeInvalid) {
      setLocalError('End date cannot be before start date.')
      return
    }

    const start = parseLocalDate(startDate)
    const end = parseLocalDate(endDate)
    const todayDate = parseLocalDate(today)
    const maxDate = parseLocalDate(maxForecastDate)

    if (start < todayDate || end > maxDate || end < start) {
      setError(FORECAST_RANGE_MESSAGE)
      return
    }

    const totalDays =
      Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)) + 1

    if (totalDays > 5) {
      setError(FORECAST_RANGE_MESSAGE)
      return
    }

    onSearch(trimmedLocation, startDate, endDate)
  }

  const handleStartDateChange = (value: string) => {
    setStartDate(value)

    if (endDate && new Date(value) > new Date(endDate)) {
      setEndDate(value)
    }
  }

  return (
    <div className={styles.searchContainer}>
      <form className={styles.searchForm} onSubmit={handleSubmit}>
        <input
          className={styles.searchInput}
          type="text"
          value={location}
          onChange={(event) => setLocation(event.target.value)}
          placeholder="Search city, ZIP, landmark, or coordinates"
          disabled={isLoading}
          aria-label="Location search"
        />

        <input
          className={styles.dateInput}
          type="date"
          value={startDate}
          min={today}
          max={maxForecastDate}
          disabled={isLoading}
          aria-label="Start date"
          onChange={(e) => {
            const newStartDate = e.target.value
            setStartDate(newStartDate)

            if (parseLocalDate(endDate) < parseLocalDate(newStartDate)) {
              setEndDate(newStartDate)
            }

            if (parseLocalDate(endDate) > parseLocalDate(maxForecastDate)) {
              setEndDate(maxForecastDate)
            }
          }}
        />

        <input
          className={styles.dateInput}
          type="date"
          value={endDate}
          min={startDate}
          max={maxForecastDate}
          onChange={(event) => setEndDate(event.target.value)}
          disabled={isLoading}
          aria-label="End date"
        />

        <button
          className={styles.searchButton}
          type="submit"
          disabled={isLoading || !location.trim() || isDateRangeInvalid}
        >
          <FiSearch />
          Search
        </button>
      </form>

      <button
        className={styles.locationButton}
        type="button"
        onClick={onCurrentLocation}
        disabled={isLoading}
      >
        <FiMapPin />
        Current Location
      </button>

      {localError && (
        <p
          style={{
            width: '100%',
            color: '#fecaca',
            fontSize: '14px',
            marginTop: '8px'
          }}
        >
          {localError}
        </p>
      )}
    </div>
  )
}

export default SearchBar