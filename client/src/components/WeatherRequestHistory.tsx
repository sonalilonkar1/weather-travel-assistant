import { FiDownload, FiTrash2, FiMapPin } from 'react-icons/fi'
import { WeatherRequest } from '../services/api'
import styles from './SavedLocations.module.css'

interface WeatherRequestHistoryProps {
  requests: WeatherRequest[]
  onSelect: (request: WeatherRequest) => void
  onDelete: (id: number) => void
  onExport: (format: 'json' | 'csv' | 'pdf') => void
  isLoading: boolean
}

export default function WeatherRequestHistory({
  requests,
  onSelect,
  onDelete,
  onExport,
  isLoading
}: WeatherRequestHistoryProps) {
  return (
    <section className={styles.savedLocations}>
      <div className={styles.header}>
        <h3>Weather Request History</h3>

        <div className={styles.exportButtons}>
          <button
            className={styles.exportBtn}
            onClick={() => onExport('json')}
            disabled={isLoading || requests.length === 0}
          >
            <FiDownload />
            JSON
          </button>

          <button
            className={styles.exportBtn}
            onClick={() => onExport('csv')}
            disabled={isLoading || requests.length === 0}
          >
            <FiDownload />
            CSV
          </button>

          <button
            className={styles.exportBtn}
            onClick={() => onExport('pdf')}
            disabled={isLoading || requests.length === 0}
          >
            <FiDownload />
            PDF
          </button>
        </div>
      </div>

      {requests.length === 0 ? (
        <div className={styles.emptyState}>
          No weather requests saved yet.
        </div>
      ) : (
        <div className={styles.locationsList}>
          {requests.map((request) => (
            <div key={request.id} className={styles.locationCard}>
              <button
                className={styles.locationContent}
                onClick={() => onSelect(request)}
                disabled={isLoading}
              >
                <div className={styles.iconWrapper}>
                  <FiMapPin />
                </div>

                <div className={styles.info}>
                  <span className={styles.locationName}>
                    {request.resolved_location}
                  </span>

                  <span className={styles.weatherInfo}>
                    {request.start_date} to {request.end_date}
                  </span>

                  <span className={styles.timestamp}>
                    Saved {new Date(request.created_at).toLocaleString()}
                  </span>
                </div>
              </button>

              <button
                className={styles.deleteBtn}
                onClick={() => onDelete(request.id)}
                disabled={isLoading}
                aria-label={`Delete ${request.resolved_location}`}
              >
                <FiTrash2 />
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}