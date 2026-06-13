import React, { useEffect, useState } from 'react'
import styles from './SavedLocations.module.css'
import { SavedLocation, deleteLocation } from '../services/api'
import { FiX, FiDownload } from 'react-icons/fi'
import { getWeatherIcon } from '../utils/weather'

interface SavedLocationsProps {
  locations: SavedLocation[] | null
  onLocationClick: (location: SavedLocation) => void
  onDelete: (id: number) => void
  onExport: (format: 'json' | 'csv') => void
  isLoading: boolean
}

export const SavedLocations: React.FC<SavedLocationsProps> = ({
  locations,
  onLocationClick,
  onDelete,
  onExport,
  isLoading
}) => {
  if (!locations || locations.length === 0) {
    return (
      <div className={styles.emptyState}>
        <p>No saved locations yet. Search for a location to save it!</p>
      </div>
    )
  }

  return (
    <div className={styles.savedLocations}>
      <div className={styles.header}>
        <h3>Saved Locations ({locations.length})</h3>
        <div className={styles.exportButtons}>
          <button
            onClick={() => onExport('json')}
            disabled={isLoading}
            title="Export as JSON"
            className={styles.exportBtn}
          >
            <FiDownload /> JSON
          </button>
          <button
            onClick={() => onExport('csv')}
            disabled={isLoading}
            title="Export as CSV"
            className={styles.exportBtn}
          >
            <FiDownload /> CSV
          </button>
        </div>
      </div>

      <div className={styles.locationsList}>
        {locations.map((location) => (
          <div key={location.id} className={styles.locationCard}>
            <button
              className={styles.locationContent}
              onClick={() => onLocationClick(location)}
              disabled={isLoading}
            >
              <div className={styles.iconWrapper}>
                {getWeatherIcon(location.icon || '0', 32)}
              </div>
              <div className={styles.info}>
                <div className={styles.locationName}>{location.location}</div>
                <div className={styles.weatherInfo}>
                  {Math.round(location.temperature)}°C • {location.description}
                </div>
                <div className={styles.timestamp}>
                  {new Date(location.created_at).toLocaleDateString()}
                </div>
              </div>
            </button>
            <button
              className={styles.deleteBtn}
              onClick={() => onDelete(location.id)}
              disabled={isLoading}
              title="Delete location"
            >
              <FiX />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
