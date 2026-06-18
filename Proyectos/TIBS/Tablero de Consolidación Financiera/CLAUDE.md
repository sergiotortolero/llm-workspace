# Tablero de Consolidación Financiera

> Formerly folder "Data-SQL-PowerBI". **Internal TIBS project** (not for a client).

## Purpose
Connect to the SQL database behind Power BI, analyze and audit its stored procedures,
and produce a "white-level" (vendor-neutral) version of it. Internal financial-consolidation
dashboard work.

## Status
Internal. Scaffolded on 2026-06-10. Connectivity not yet established (read-only by default).
Detailed scope to be expanded later (we will resume the SQL + Power BI + white-label thread
discussed at the start of the workspace setup).

## Stack / Connectivity
- DB engine: TBD (likely SQL Server / Azure SQL). See `../../../docs/setup/data-connectivity.md`.
- Connectors: Microsoft SQL MCP Server (executes stored procedures) + Power BI MCP.
  Templates in `../../../.mcp.json.example`. Decision pending in `docs/adr/` (see root ADR-0002).

## Rules
- Default to **read-only**. Any write/DDL requires explicit confirmation from Sergio.
- Never commit credentials/connection strings. Use environment variables.
- Handled by the `data-platform` subagent. Audits go in `docs/audits/` using the template.

## "White-level" = white-label (DECIDED 2026-06-10)
Generalize the DB/stored procedures: abstract proprietary or client-specific logic,
names, and hardcoded values into a reusable vendor-neutral baseline, plus a mapping of
what was generalized. See root ADR-0002.

## Open decisions (needed to connect for real)
- [ ] DB engine + hosting (on-prem SQL Server vs Azure SQL) — discover via Power BI
      Desktop → Transform data → Data source settings (see ../../../docs/setup/data-connectivity.md).
- [ ] Connection string / credentials.
- [ ] Power BI tier (Premium / PPU / Fabric → XMLA availability).
- [ ] Access level (read-only vs read-write).
