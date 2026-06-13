import React from 'react'
import styles from './ErrorMessage.module.css'
import { FiAlertCircle, FiX } from 'react-icons/fi'

interface ErrorMessageProps {
  message: string
  onClose: () => void
  type?: 'error' | 'warning' | 'info'
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onClose,
  type = 'error'
}) => {
  return (
    <div className={`${styles.errorContainer} ${styles[type]}`}>
      <div className={styles.content}>
        <FiAlertCircle className={styles.icon} />
        <p className={styles.message}>{message}</p>
      </div>
      <button
        className={styles.closeBtn}
        onClick={onClose}
        aria-label="Close error message"
      >
        <FiX />
      </button>
    </div>
  )
}
