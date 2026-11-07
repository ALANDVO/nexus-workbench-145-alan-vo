import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from './App'

describe('App', () => {
  const mockHealth = { status: 'ok', service: 'nexus-workbench-api', version: '1.0.0' }
  const mockPlugins = {
    plugins: [
      { id: 'bio-research', name: 'Bio Research', description: 'Bioinformatics workflows', version: '1.0.0', author: 'Alan Vo', status: 'active', tags: ['bioinformatics'] },
      { id: 'marketing', name: 'Marketing', description: 'Content creation tools', version: '1.0.0', author: 'Alan Vo', status: 'active', tags: ['marketing'] },
    ],
    total: 2,
  }

  beforeEach(() => {
    vi.spyOn(window, 'fetch').mockImplementation((url) => {
      if (url.toString().includes('/api/v1/health')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockHealth),
        } as Response)
      }
      if (url.toString().includes('/api/v1/plugins')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockPlugins),
        } as Response)
      }
      return Promise.resolve({
        ok: false,
        status: 404,
      } as Response)
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders title and subtitle', () => {
    render(<App />)
    expect(screen.getByText('Nexus Workbench')).toBeInTheDocument()
    expect(screen.getByText('AI/ML Plugin Catalog for Claude Cowork')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    render(<App />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('displays health data after fetch', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('ok')).toBeInTheDocument()
      expect(screen.getByText('nexus-workbench-api')).toBeInTheDocument()
      expect(screen.getByText('1.0.0')).toBeInTheDocument()
    })
  })
})
