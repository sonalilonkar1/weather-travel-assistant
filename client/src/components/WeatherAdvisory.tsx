import styles from './WeatherAdvisory.module.css'

interface WeatherAdvisoryProps {
  tips: string[] | undefined
}

function getAdvisoryTitle(tip: string) {
  if (tip.toLowerCase().includes('heat')) return 'Heat Advisory'
  if (tip.toLowerCase().includes('snow')) return 'Snow Advisory'
  if (tip.toLowerCase().includes('wind')) return 'Wind Advisory'
  if (tip.toLowerCase().includes('rain')) return 'Rain Advisory'
  if (tip.toLowerCase().includes('freeze')) return 'Freeze Advisory'
  return 'Weather Advisory'
}

export default function WeatherAdvisory({ tips }: WeatherAdvisoryProps) {
  if (!tips || tips.length === 0) {
    return null
  }

  const importantTip =
    tips.find((tip) =>
      ['heat', 'snow', 'wind', 'rain', 'freeze'].some((keyword) =>
        tip.toLowerCase().includes(keyword)
      )
    ) || tips[0]

  return (
    <section className={styles.advisory}>
      <h3 className={styles.title}>⚠️ {getAdvisoryTitle(importantTip)}</h3>
      <p className={styles.message}>{importantTip}</p>
      <p className={styles.source}>Generated from current and forecast weather conditions</p>
    </section>
  )
}