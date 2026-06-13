import { WiDaySunny, WiCloudy, WiRain, WiSnow, WiWindy, WiDayCloudy, WiNightCloudy, WiDayRain, WiNightRain, WiThunderstorm, WiFog } from 'react-icons/wi'
import React from 'react'

export const getWeatherIcon = (code: string, size: number = 40): React.ReactNode => {
  const iconProps = { size, color: '#fbbf24' }

  const iconMap: Record<string, React.ReactNode> = {
    '0': <WiDaySunny {...iconProps} />,         // Clear
    '1': <WiDayCloudy {...iconProps} />,        // Partly cloudy
    '2': <WiCloudy {...iconProps} />,           // Cloudy
    '3': <WiCloudy {...iconProps} />,           // Overcast
    '45': <WiFog {...iconProps} />,             // Foggy
    '48': <WiFog {...iconProps} />,             // Depositing rime fog
    '51': <WiDayRain {...iconProps} />,         // Light drizzle
    '53': <WiDayRain {...iconProps} />,         // Moderate drizzle
    '55': <WiDayRain {...iconProps} />,         // Dense drizzle
    '61': <WiRain {...iconProps} />,            // Slight rain
    '63': <WiRain {...iconProps} />,            // Moderate rain
    '65': <WiRain {...iconProps} />,            // Heavy rain
    '71': <WiSnow {...iconProps} />,            // Slight snow
    '73': <WiSnow {...iconProps} />,            // Moderate snow
    '75': <WiSnow {...iconProps} />,            // Heavy snow
    '77': <WiSnow {...iconProps} />,            // Snow grains
    '80': <WiRain {...iconProps} />,            // Slight rain showers
    '81': <WiRain {...iconProps} />,            // Moderate rain showers
    '82': <WiRain {...iconProps} />,            // Violent rain showers
    '85': <WiSnow {...iconProps} />,            // Slight snow showers
    '86': <WiSnow {...iconProps} />,            // Heavy snow showers
    '95': <WiThunderstorm {...iconProps} />,    // Thunderstorm
    '96': <WiThunderstorm {...iconProps} />,    // Thunderstorm with hail
    '99': <WiThunderstorm {...iconProps} />,    // Thunderstorm with heavy hail
  }

  return iconMap[code] || <WiDaySunny {...iconProps} />
}

export const getWeatherDescription = (code: string): string => {
  const descriptions: Record<string, string> = {
    '0': 'Clear',
    '1': 'Partly Cloudy',
    '2': 'Cloudy',
    '3': 'Overcast',
    '45': 'Foggy',
    '48': 'Rime Fog',
    '51': 'Light Drizzle',
    '53': 'Moderate Drizzle',
    '55': 'Heavy Drizzle',
    '61': 'Slight Rain',
    '63': 'Moderate Rain',
    '65': 'Heavy Rain',
    '71': 'Slight Snow',
    '73': 'Moderate Snow',
    '75': 'Heavy Snow',
    '77': 'Snow Grains',
    '80': 'Rain Showers',
    '81': 'Heavy Rain Showers',
    '82': 'Violent Rain Showers',
    '85': 'Snow Showers',
    '86': 'Heavy Snow Showers',
    '95': 'Thunderstorm',
    '96': 'Thunderstorm + Hail',
    '99': 'Thunderstorm + Heavy Hail',
  }

  return descriptions[code] || 'Unknown'
}

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  })
}

export const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

export const downloadFile = (blob: Blob, filename: string): void => {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}
