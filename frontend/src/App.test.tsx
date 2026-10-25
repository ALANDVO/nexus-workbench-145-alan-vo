import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from './App'

describe('App', () => {
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
    const mockHealth = { status: 'ok', service: 'nexus-workbench-api', version: '1.0.0' }
    vi.spyOn(window, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockHealth),
    } as Response)

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('ok')).toBeInTheDocument()
      expect(screen.getByText('nexus-workbench-api')).toBeInTheDocument()
      expect(screen.getByText('1.0.0')).toBeInTheDocument()
    })
  })
})
