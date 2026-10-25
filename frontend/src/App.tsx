import { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState<{ status: string; service: string; version: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/v1/health')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => {
        setHealth(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Nexus Workbench</h1>
        <p style={styles.subtitle}>AI/ML Plugin Catalog for Claude Cowork</p>
      </header>
      <main style={styles.main}>
        <section style={styles.card}>
          <h2>Backend Health</h2>
          {loading && <p>Loading...</p>}
          {error && <p style={styles.error}>Error: {error}</p>}
          {health && (
            <div>
              <p><strong>Status:</strong> <span style={styles.badgeOk}>{health.status}</span></p>
              <p><strong>Service:</strong> {health.service}</p>
              <p><strong>Version:</strong> {health.version}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    padding: '2rem',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    background: '#fafafa',
  },
  header: {
    maxWidth: '800px',
    margin: '0 auto 2rem',
    textAlign: 'center',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 700,
    color: '#1a1a2e',
    marginBottom: '0.5rem',
  },
  subtitle: {
    fontSize: '1.1rem',
    color: '#666',
    marginBottom: '2rem',
  },
  main: {
    maxWidth: '800px',
    margin: '0 auto',
  },
  card: {
    background: 'white',
    padding: '1.5rem',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  error: {
    color: '#c62828',
  },
  badgeOk: {
    background: '#e8f5e9',
    color: '#2e7d32',
    padding: '0.25rem 0.75rem',
    borderRadius: '9999px',
    fontSize: '0.875rem',
    fontWeight: 500,
  },
}

export default App
