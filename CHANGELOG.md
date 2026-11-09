# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

### Added
- **Enhancement to skill-browser**: Renamed misleading `filteredSkills` variable to `displaySkills` in SkillBrowser.tsx (filtering happens server-side via API, not client-side)
- **Accessibility improvement**: Added keyboard navigation (ArrowUp/ArrowDown) and ARIA attributes (`role="listbox"`, `role="option"`, `aria-selected`) to skill list

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — work-in-progress checkpoint

### Added
- Skill browser feature with stability filtering (experimental/stable/deprecated)
- Skill models (Skill, SkillStability, SkillListResponse) with stability enum
- Skill catalog service loading SKILL.md files with frontmatter from plugins/*/skills/
- Skills API endpoints: GET /api/v1/skills (with plugin_id, stability filters), GET /api/v1/skills/{plugin_id}/{skill_id}/content
- Sample skills across all three plugins: bio-research (2), marketing (2), productivity (2)
- SkillBrowser frontend component with:
  - Plugin filter dropdown (all, bio-research, marketing, productivity)
  - Stability filter dropdown (all, experimental, stable, deprecated)
  - Skills list with stability badges (color-coded: orange/green/gray)
  - Skill detail panel showing full markdown content
- Backend tests for skills API (list, filter by plugin, filter by stability, get content)
- Frontend tests updated to mock both health and plugins endpoints
- python-frontmatter dependency for parsing SKILL.md frontmatter

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

### Added
- Initial FastAPI backend skeleton with health endpoint
- React + TypeScript + Vite frontend with health display
- Docker Compose with backend, frontend, Keycloak
- Backend tests (pytest + httpx)
- Frontend tests (vitest + React Testing Library)
- GitHub Actions CI workflow
- Configuration via environment variables
- MIT License
- Plugin catalog API with YAML-based plugin configuration
- Plugin models (Plugin, PluginStatus, PluginListResponse)
- Plugin catalog service loading plugins from plugins/ directory
- Sample plugin configs: bio-research, productivity, marketing
- Backend tests for plugin catalog endpoint
- PluginCatalog frontend component with responsive grid layout
- Plugin cards displaying name, description, version, status, tags, and repository link
- MIT License

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
