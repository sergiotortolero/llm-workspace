# ADR-0002: Data connectivity for SQL and Power BI (and "white-level" deliverable)

| Field    | Value                          |
|----------|--------------------------------|
| Status   | Proposed (pending Sergio's input) |
| Date     | 2026-06-10                     |
| Deciders | Sergio Tortolero, Claude       |
| Project  | Tablero de Consolidación Financiera (interno) |

## Context
Sergio needs to connect to a SQL database that backs Power BI and contains stored
procedures, to analyze, audit, and produce a "white-level" version. As of 2026-06,
Microsoft ships official MCP servers (Public Preview, Ignite Nov 2025):
- **SQL MCP Server** (Data API Builder) — lists objects, reads data, executes SPs.
- **Power BI MCP** — remote (DAX queries) and local modeling (TMDL in PBIP).

## Decision (proposed)
Prefer the **Microsoft SQL MCP Server** for stored-procedure analysis, with read-only
access by default. Use the **Power BI Modeling MCP** if/when we touch the semantic model.
Fallback to read-only `sqlcmd`/Python scripts until MCP is installed.

**"White-level" = white-label (vendor-neutral) — DECIDED (2026-06-10).** The deliverable
is a generalized version of the database/stored procedures where proprietary or
client-specific logic is abstracted so it can be reused as a neutral baseline. The audit
will (1) catalog each object, (2) flag proprietary/client-specific logic, names, and
hardcoded values, and (3) produce the abstracted white-label version alongside a mapping
of what was generalized.

## Open questions (block acceptance)
1. **Engine & hosting:** SQL Server on-prem vs Azure SQL vs other.
2. **Credentials / connection string** and access method.
3. **Power BI tier:** Premium / PPU / Fabric? (determines XMLA availability).
4. **"White-level" definition** — RESOLVED: option (d) **vendor-neutral / white-label**.
5. **Access level:** read-only audit vs. read-write.

## Consequences
Official Microsoft servers reduce risk and avoid fabricated/third-party tooling. XMLA
features depend on the Power BI tier. The "white-level" approach changes the entire
deliverable, so it must be decided before audit work produces it.

## References
- https://learn.microsoft.com/en-us/sql/mcp/
- https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview
- https://github.com/microsoft/powerbi-modeling-mcp
