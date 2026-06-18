# Shelly - Censo de Cargas

## Purpose
Local telemetry pipeline for a **Shelly Pro 3EM** energy meter: ingest readings, persist
them to PostgreSQL, apply non-destructive corrections, and visualize consumption in a
**Streamlit** dashboard. Fully local (no cloud dependency).

## Stack
- **Docker Compose** orchestrating: PostgreSQL, a Python **receiver API** (`/shelly`,
  health at `:8765`), **Adminer** (`:8080`), and a **Streamlit** dashboard (`:8501`).
- **Python** tools: `tools/curator` (materialize corrections → CSV / materialized table),
  `tools/importer` (ingest the Shelly device's historical CSV export).
- **Shelly JS** script (`scripts/shelly_export.js`) running on the device, POSTing total
  energy (Wh) every 60s to the receiver.
- Native **`dist/shelly_launcher.exe`** that boots Docker + opens the dashboard.

## Data model (key tables)
- `readings_raw` — raw readings, never edited.
- `correction_windows` — manual correction rules (reversed CT, missing voltage, etc.).
- `readings_curated` (view) + `readings_curated_materialized` — corrected data.

## Folders
`dashboard/` (Streamlit) · `db/` (SQL schema/migrations) · `receiver/` (Python API) ·
`scripts/` (Shelly JS) · `tools/` (curator, importer) · `dist/` (launcher .exe).

## Notes
- See `README.md` and `guia_shelly_docker_antigravity.md` for full setup (in Spanish).
- **Cross-reference:** this project already uses Streamlit + Postgres — a useful reference
  pattern for the `Corrections Module PMR` project.

## Rules
- Respond to Sergio in Spanish; code, comments, and docs in English.
- Raw data is never edited — corrections go through `correction_windows`.
