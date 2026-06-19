# Corrections Module PMR - Streamlit

## Purpose
**Work project — TIBS, client Chubb.** Evaluate and (if justified) re-platform an existing React application to **Streamlit**
(Python data-app framework). The first deliverable is a functional analysis of the
implications and the alternatives that can fulfill what the React code does.

## Status
Scaffolded on 2026-06-18. **Evaluation phase** — no migration started.
This is a *re-platform* (language + execution model + UI paradigm change), not a refactor.
**Priority: highest / urgent.** Sergio has an **analysis & architecture document** (to be
shared) that will resolve the open questions below (audience, data home, rich-grid, auth)
and let us produce the migration plan.

## Source
- React app: `C:\Users\srtor\Downloads\chubb_policy_validation_system_v54_clearer_rule_ui.tsx`
  (1888 lines, single-file React + Tailwind, SheetJS). "PMR Corrections Module" — internal
  Chubb LATAM tool to review/correct insurance policy data for the Price Monitor Report.
  **No backend** (1000 policies generated in-browser; state resets on refresh).
- Streamlit target: Python. See `docs/adr/0001-react-to-streamlit-evaluation.md` for the
  full feature-by-feature analysis.

## Cómo se lleva este proyecto (nueva estructura)
- **Agente dedicado:** `.claude/agents/streamlit-migrator.md` (se activa al abrir Claude Code
  en esta carpeta). Porta el motor de reglas a Python, diseña backend/datos/auth y construye por fases.
- **Documento de análisis y arquitectura:** colócalo en `docs/architecture/` (ver su README).
  Eso desbloquea las decisiones abiertas y el plan de migración.
- **Apoyo:** skills globales `senior-architect`, `senior-backend`, `senior-qa`; agentes `python-pro`, `data-engineer`.

## Rules
- Respond to Sergio in Spanish; code, comments, and docs in English.
- Decision goes in an ADR (`docs/adr/0001-...`) before any migration work.
- A feature/migration plan needs a PRD in `docs/prd/` once direction is chosen.

## Open questions (block the decision)
- [ ] Where is the React code (path/repo) and what is its size/shape?
- [ ] Is the app customer-facing or an internal/data tool?
- [ ] How custom is the UI (branding, complex interactions) vs. mostly forms/tables/charts?
- [ ] Why Streamlit specifically (team is Python-first? data/ML heavy? simplify maintenance?)
- [ ] Is there a backend/API already, or is all logic in the React frontend?

## Next steps
1. Receive the React code → inventory its features and dependencies.
2. Complete the evaluation ADR with a recommendation.
3. If Streamlit (or alternative) is chosen → PRD + migration plan.
