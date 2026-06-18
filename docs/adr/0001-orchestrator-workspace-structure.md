# ADR-0001: Orchestrator workspace structure and domain subagents

| Field    | Value                          |
|----------|--------------------------------|
| Status   | Accepted                       |
| Date     | 2026-06-10                     |
| Deciders | Sergio Tortolero, Claude       |
| Project  | Orchestrator                   |

## Context
Sergio runs `D:\LLM's` as a PM-orchestrator root over multiple projects (Kibo,
AppConsulta, Shelly, and new ones). He wants a reusable Claude Code structure from which
he can invoke specialized agents per task, across three domains: PM documentation,
data (SQL + Power BI), and web platform construction (Kibo, Mouna).

## Decision
We will keep the root as an **orchestration layer** (config, templates, memory) and model
each domain as a Claude Code **subagent** under `.claude/agents/`:
- `pm-docs` — minutes and PM documentation.
- `data-platform` — SQL + Power BI analysis/audit.
- `web-architect` — Kibo and Mouna web platforms.

Shared **templates** live in `templates/`, reusable **slash commands** in
`.claude/commands/`, and durable **memory** in the Claude memory directory. A PowerShell
script (`scripts/New-ProjectDocs.ps1`) scaffolds each project's `docs/` structure.

## Options Considered
1. **Subagents per domain (chosen)** — clean routing, reusable, easy to polish.
2. One mega-prompt in CLAUDE.md — no isolation, hard to scale.
3. Separate Claude Code instances per project only — loses the orchestration layer.

## Consequences
**Positive:** consistent structure across projects; Sergio can route work by naming a
domain; templates enforce the PRD-before-build / ADR-before-architecture rules.
**Trade-offs:** more files to maintain; subagents must be kept in sync with skills.
**Follow-ups:**
- [ ] Confirm data-connectivity decision (ADR-0002).
- [ ] Add Mouna product context once defined.
