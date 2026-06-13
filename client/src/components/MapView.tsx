import React from 'react'
import styles from './MapView.module.css'

interface MapViewProps {
  latitude: number
  longitude: number
  city: string
}

const googleMapsKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY
export const MapView: React.FC<MapViewProps> = ({ latitude, longitude, city }) => {
  if (!googleMapsKey) {
    return (
      <div className={styles.mapContainer}>
        <h3 className={styles.title}>Location Map</h3>
        <p>Google Maps API key is not configured.</p>
      </div>
    )
  }
  const mapUrl = `https://www.google.com/maps/embed/v1/view?key=${googleMapsKey}&center=${latitude},${longitude}&zoom=10`
  return (
    <div className={styles.mapContainer}>
      <h3 className={styles.title}>Location Map</h3>
      <iframe
        className={styles.iframe}
        title={`Map of ${city}`}
        src={mapUrl}
        loading="lazy"
        allowFullScreen
      />
    </div>
  )
}

