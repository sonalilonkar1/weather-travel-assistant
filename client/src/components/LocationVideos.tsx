import { useEffect, useState } from 'react'
import { getLocationVideos, YouTubeVideo } from '../services/api'
import styles from './LocationVideos.module.css'

interface LocationVideosProps {
  location: string
}

function LocationVideos({ location }: LocationVideosProps) {
  const [videos, setVideos] = useState<YouTubeVideo[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchVideos = async () => {
      if (!location) {
        setVideos([])
        return
      }

      setIsLoading(true)
      setError('')

      try {
        const data = await getLocationVideos(location)
        setVideos(data)
      } catch {
        setError('Unable to load location videos right now.')
        setVideos([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchVideos()
  }, [location])

  if (!location) {
    return null
  }

  return (
    <section className={styles.videosSection}>
      <div className={styles.header}>
        <div>
          <h2>Explore {location}</h2>
          <p>Travel videos and local guides for this destination</p>
        </div>
      </div>

      {isLoading && <p className={styles.message}>Loading videos...</p>}

      {error && <p className={styles.error}>{error}</p>}

      {!isLoading && !error && videos.length === 0 && (
        <p className={styles.message}>No videos found for this location.</p>
      )}

      <div className={styles.videoGrid}>
        {videos.map((video) => (
          <article key={video.video_id} className={styles.videoCard}>
            <div className={styles.videoFrame}>
              <iframe
                src={video.embed_url}
                title={video.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>

            <div className={styles.videoContent}>
              <h3>{video.title}</h3>
              <p>{video.channel_title}</p>
              <a
                href={video.video_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Watch on YouTube
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}

export default LocationVideos