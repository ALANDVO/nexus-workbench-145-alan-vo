import { useState, useEffect } from 'react'

interface Plugin {
  id: string
  name: string
  description: string
  version: string
  author: string
  status: string
  tags: string[]
  repository?: string
  homepage?: string
  license?: string
}

interface PluginListResponse {
  plugins: Plugin[]
  total: number
}

export function PluginCatalog() {
  const [plugins, setPlugins] = useState<Plugin[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/v1/plugins')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data: PluginListResponse) => {
        setPlugins(data.plugins)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <p>Loading plugins...</p>
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>

  return (
    <section style={styles.section}>
      <h2>Plugin Catalog ({plugins.length})</h2>
      <div style={styles.grid}>
        {plugins.map(plugin => (
          <article key={plugin.id} style={styles.card}>
            <h3 style={styles.name}>{plugin.name}</h3>
            <p style={styles.description}>{plugin.description}</p>
            <div style={styles.meta}>
              <span style={styles.badge}>v{plugin.version}</span>
              <span style={{ ...styles.badge, background: '#e3f2fd', color: '#1565c0' }}>{plugin.status}</span>
            </div>
            <div style={styles.tags}>
              {plugin.tags.map(tag => (
                <span key={tag} style={styles.tag}>{tag}</span>
              ))}
            </div>
            {plugin.repository && (
              <a href={plugin.repository} target="_blank" rel="noopener noreferrer" style={styles.link}>
                Repository
              </a>
            )}
          </article>
        ))}
      </div>
    </section>
  )
}

const styles: Record<string, React.CSSProperties> = {
  section: {
    marginTop: '2rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '1rem',
  },
  card: {
    background: 'white',
    padding: '1.5rem',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    border: '1px solid #eee',
  },
  name: {
    margin: '0 0 0.5rem',
    fontSize: '1.1rem',
    color: '#1a1a2e',
  },
  description: {
    margin: '0 0 1rem',
    color: '#555',
    fontSize: '0.9rem',
    lineHeight: 1.5,
  },
  meta: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.75rem',
  },
  badge: {
    padding: '0.2rem 0.6rem',
    borderRadius: '9999px',
    fontSize: '0.75rem',
    fontWeight: 500,
    background: '#e8f5e9',
    color: '#2e7d32',
  },
  tags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.4rem',
    marginBottom: '1rem',
  },
  tag: {
    background: '#f5f5f5',
    padding: '0.15rem 0.5rem',
    borderRadius: '4px',
    fontSize: '0.7rem',
    color: '#666',
  },
  link: {
    fontSize: '0.85rem',
    color: '#1976d2',
    textDecoration: 'none',
  },
}
