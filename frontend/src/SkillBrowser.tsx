import { useState, useEffect } from 'react'

interface Skill {
  id: string
  name: string
  description: string
  plugin_id: string
  stability: 'experimental' | 'stable' | 'deprecated'
  tags: string[]
  file_path: string
}

interface SkillListResponse {
  skills: Skill[]
  total: number
}

type StabilityFilter = 'all' | 'experimental' | 'stable' | 'deprecated'

export function SkillBrowser() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [stabilityFilter, setStabilityFilter] = useState<StabilityFilter>('all')
  const [pluginFilter, setPluginFilter] = useState<string>('all')
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null)
  const [skillContent, setSkillContent] = useState<string>('')

  const plugins = ['all', 'bio-research', 'marketing', 'productivity']

  useEffect(() => {
    fetchSkills()
  }, [stabilityFilter, pluginFilter])

  const fetchSkills = async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      if (pluginFilter !== 'all') params.append('plugin_id', pluginFilter)
      if (stabilityFilter !== 'all') params.append('stability', stabilityFilter)

      const response = await fetch(`/api/v1/skills?${params.toString()}`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data: SkillListResponse = await response.json()
      setSkills(data.skills)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const fetchSkillContent = async (skill: Skill) => {
    setSelectedSkill(skill)
    setSkillContent('Loading...')
    try {
      const response = await fetch(`/api/v1/skills/${skill.plugin_id}/${skill.id}/content`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const content = await response.text()
      setSkillContent(content)
    } catch (err) {
      setSkillContent(`Error loading content: ${err instanceof Error ? err.message : 'Unknown error'}`)
    }
  }

  const filteredSkills = skills

  if (loading) return <p>Loading skills...</p>
  if (error) return <p style={{ color: 'red' }}>Error: {error}</p>

  return (
    <section style={styles.section}>
      <h2 style={styles.title}>Skill Browser</h2>

      <div style={styles.filters}>
        <div style={styles.filterGroup}>
          <label style={styles.label}>Plugin: </label>
          <select
            value={pluginFilter}
            onChange={(e) => setPluginFilter(e.target.value)}
            style={styles.select}
          >
            {plugins.map((p) => (
              <option key={p} value={p}>{p === 'all' ? 'All Plugins' : p}</option>
            ))}
          </select>
        </div>

        <div style={styles.filterGroup}>
          <label style={styles.label}>Stability: </label>
          <select
            value={stabilityFilter}
            onChange={(e) => setStabilityFilter(e.target.value as StabilityFilter)}
            style={styles.select}
          >
            <option value="all">All</option>
            <option value="experimental">Experimental</option>
            <option value="stable">Stable</option>
            <option value="deprecated">Deprecated</option>
          </select>
        </div>
      </div>

      <div style={styles.layout}>
        <div style={styles.skillsList}>
          <h3 style={styles.listTitle}>Skills ({filteredSkills.length})</h3>
          {filteredSkills.length === 0 ? (
            <p style={styles.empty}>No skills found matching filters.</p>
          ) : (
            <ul style={styles.list}>
              {filteredSkills.map((skill) => (
                <li key={skill.id} style={styles.listItem}>
                  <button
                    onClick={() => fetchSkillContent(skill)}
                    style={{
                      ...styles.skillButton,
                      background: selectedSkill?.id === skill.id ? '#e3f2fd' : 'white',
                      borderColor: selectedSkill?.id === skill.id ? '#1976d2' : '#e0e0e0',
                    }}
                  >
                    <div style={styles.skillHeader}>
                      <span style={styles.skillName}>{skill.name}</span>
                      <span style={{
                        ...styles.stabilityBadge,
                        background: stabilityColors[skill.stability].bg,
                        color: stabilityColors[skill.stability].fg,
                      }}>
                        {skill.stability}
                      </span>
                    </div>
                    <div style={styles.skillMeta}>
                      <span style={styles.pluginTag}>{skill.plugin_id}</span>
                      {skill.tags.slice(0, 3).map((tag) => (
                        <span key={tag} style={styles.tag}>{tag}</span>
                      ))}
                      {skill.tags.length > 3 && (
                        <span style={styles.tag}>+{skill.tags.length - 3} more</span>
                      )}
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div style={styles.detailPanel}>
          {selectedSkill ? (
            <div style={styles.detail}>
              <div style={styles.detailHeader}>
                <h3 style={styles.detailTitle}>{selectedSkill.name}</h3>
                <span style={{
                  ...styles.stabilityBadge,
                  background: stabilityColors[selectedSkill.stability].bg,
                  color: stabilityColors[selectedSkill.stability].fg,
                }}>
                  {selectedSkill.stability}
                </span>
              </div>
              <p style={styles.detailPlugin}>Plugin: {selectedSkill.plugin_id}</p>
              <p style={styles.detailDescription}>{selectedSkill.description}</p>
              <div style={styles.detailTags}>
                {selectedSkill.tags.map((tag) => (
                  <span key={tag} style={styles.tag}>{tag}</span>
                ))}
              </div>
              <div style={styles.content}>
                <h4>Skill Content (Markdown)</h4>
                <pre style={styles.contentPre}>{skillContent}</pre>
              </div>
            </div>
          ) : (
            <p style={styles.empty}>Select a skill to view details</p>
          )}
        </div>
      </div>
    </section>
  )
}

const stabilityColors: Record<string, { bg: string; fg: string }> = {
  experimental: { bg: '#fff3e0', fg: '#e65100' },
  stable: { bg: '#e8f5e9', fg: '#2e7d32' },
  deprecated: { bg: '#fafafa', fg: '#757575' },
}

const styles: Record<string, React.CSSProperties> = {
  section: {
    marginTop: '2rem',
  },
  title: {
    marginBottom: '1rem',
    fontSize: '1.5rem',
    color: '#1a1a2e',
  },
  filters: {
    display: 'flex',
    gap: '1.5rem',
    marginBottom: '1.5rem',
    flexWrap: 'wrap',
  },
  filterGroup: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  label: {
    fontWeight: 500,
    color: '#333',
  },
  select: {
    padding: '0.375rem 0.75rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    background: 'white',
    fontSize: '0.875rem',
  },
  layout: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '1.5rem',
  },
  skillsList: {
    background: 'white',
    padding: '1rem',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    minHeight: '400px',
  },
  listTitle: {
    marginTop: 0,
    marginBottom: '1rem',
    fontSize: '1.1rem',
    color: '#1a1a2e',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
    maxHeight: '500px',
    overflowY: 'auto',
  },
  listItem: {
    marginBottom: '0.5rem',
  },
  skillButton: {
    width: '100%',
    textAlign: 'left',
    padding: '0.75rem',
    border: '1px solid #e0e0e0',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.15s ease',
  },
  skillHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.5rem',
  },
  skillName: {
    fontWeight: 600,
    fontSize: '0.9375rem',
    color: '#1a1a2e',
  },
  stabilityBadge: {
    padding: '0.125rem 0.5rem',
    borderRadius: '9999px',
    fontSize: '0.75rem',
    fontWeight: 600,
    textTransform: 'capitalize',
  },
  skillMeta: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.375rem',
    fontSize: '0.75rem',
    color: '#666',
  },
  pluginTag: {
    fontWeight: 500,
    color: '#1976d2',
  },
  tag: {
    background: '#f0f0f0',
    padding: '0.125rem 0.375rem',
    borderRadius: '4px',
  },
  empty: {
    color: '#999',
    textAlign: 'center',
    padding: '2rem',
  },
  detailPanel: {
    background: 'white',
    padding: '1rem',
    borderRadius: '8px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    minHeight: '400px',
  },
  detail: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  detailHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '1rem',
  },
  detailTitle: {
    margin: 0,
    fontSize: '1.25rem',
    color: '#1a1a2e',
  },
  detailPlugin: {
    margin: 0,
    fontSize: '0.875rem',
    color: '#1976d2',
    fontWeight: 500,
  },
  detailDescription: {
    margin: 0,
    color: '#444',
    lineHeight: 1.6,
  },
  detailTags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.375rem',
  },
  content: {
    marginTop: '1rem',
    flex: 1,
    overflowY: 'auto',
  },
  contentPre: {
    background: '#fafafa',
    padding: '1rem',
    borderRadius: '6px',
    border: '1px solid #e0e0e0',
    fontSize: '0.8125rem',
    lineHeight: 1.6,
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
    maxHeight: '300px',
    overflowY: 'auto',
    fontFamily: 'inherit',
  },
}
