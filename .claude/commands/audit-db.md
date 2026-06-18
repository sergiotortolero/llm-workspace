---
description: Run the SQL/Power BI database audit workflow (inventory, SP catalog, findings, action plan)
argument-hint: [database or scope, optional]
---
Use the `data-platform` agent to audit the database for scope: $ARGUMENTS

Follow the workflow in the agent definition and the template at `templates/db-audit-template.md`:
1. Confirm connectivity (SQL MCP Server, or read-only scripts) — see `Proyectos/TIBS/Tablero de Consolidación Financiera/docs/setup/data-connectivity.md` if present, else the root `docs/setup/data-connectivity.md`.
2. Inventory objects, build the stored-procedure catalog, and record findings by category (Security, Performance, Maintainability, Data Integrity).
3. Before producing the "white-level" deliverable, confirm its exact definition with Sergio and record it in an ADR.
4. Save the audit to `Proyectos/TIBS/Tablero de Consolidación Financiera/docs/audits/`.

Default to read-only access. Any write/DDL requires explicit confirmation.
