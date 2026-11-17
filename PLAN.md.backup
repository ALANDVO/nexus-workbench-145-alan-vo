# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

skill-browser

## Roadmap

### skeleton — FastAPI/React skeleton with health endpoint

Status: done

Acceptance:
- FastAPI backend starts and serves /health
- React frontend builds and serves on dev server
- Docker compose runs both services
- Backend tests pass (pytest)
- Frontend tests pass (vitest)

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/api/v1/health.py`, `backend/requirements.txt`, `backend/Dockerfile`, `backend/.dockerignore`, `backend/tests/test_health.py`, `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.ts`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`, `frontend/index.html`, `frontend/vitest.config.ts`, `frontend/src/test-setup.ts`, `frontend/src/App.test.tsx`, `frontend/Dockerfile`, `frontend/nginx.conf`, `frontend/.dockerignore`, `compose.yaml`, `.env.example`, `.gitignore`, `.github/workflows/ci.yml`, `README.md`, `LICENSE`, `CHANGELOG.md`, `portfolio.json`, `pyproject.toml`

Tests: `backend/tests/test_health.py`, `frontend/src/App.test.tsx`

### plugin-catalog — Plugin catalog API and UI

Status: done

Acceptance:
- API returns list of plugins from YAML configs
- UI displays plugin cards with name, description, status

Implementation: `backend/app/models/plugin.py`, `backend/app/services/plugin_catalog.py`, `backend/app/api/v1/plugins.py`, `backend/app/main.py`, `plugins/bio-research/plugin.yaml`, `plugins/productivity/plugin.yaml`, `plugins/marketing/plugin.yaml`, `frontend/src/PluginCatalog.tsx`, `frontend/src/App.tsx`

Tests: `backend/tests/test_plugins.py`

### skill-browser — Skill browser with stability filtering

Status: done

Acceptance:
- API returns skills with stability frontmatter
- UI filters skills by experimental/stable/deprecated
- Skill detail view shows full markdown

Implementation: `backend/app/models/skill.py`, `backend/app/services/skill_catalog.py`, `backend/app/api/v1/skills.py`, `backend/app/main.py`, `backend/app/models/__init__.py`, `backend/tests/test_skills.py`, `plugins/bio-research/skills/generate-samplesheet/SKILL.md`, `plugins/bio-research/skills/run-sarek/SKILL.md`, `plugins/marketing/skills/content-quality/SKILL.md`, `plugins/marketing/skills/seo-optimizer/SKILL.md`, `plugins/productivity/skills/daily-briefing/SKILL.md`, `plugins/productivity/skills/task-automation/SKILL.md`, `frontend/src/SkillBrowser.tsx`, `frontend/src/App.tsx`

Tests: `backend/tests/test_skills.py`, `frontend/src/App.test.tsx`

### issue-tracker — GitHub issue sync and display

Status: planned

Acceptance:
- Background sync fetches issues from upstream repo
- UI displays issues with labels, status, comments
- Filter by plugin/domain

### auth-oidc — OIDC authentication with Keycloak

Status: planned

Acceptance:
- Login redirects to Keycloak
- Callback exchanges code for tokens
- Protected endpoints require valid session
- Logout clears session

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
