# Project Constitution — Sergio Tortolero / TIBS Orchestration Workspace

<!--
  PLACEMENT: workspace root → D:\LLM's\constitution.md
  REFERENCED FROM: root CLAUDE.md via `@constitution.md`
  Version 1.1 — 2026-06-23 — Global immutable laws.
  Project-level files may ADD stricter rules; they may NEVER relax these.
-->

## Priority order
When rules conflict, obey in this order:
1. Security & data protection
2. Client / legal obligations
3. Evidence & correctness
4. Process (PRD / ADR)
5. Style & language

A higher number never overrides a lower one.

## Article 1 — Security & secrets (HARD)
- NEVER write secrets, API keys, passwords, tokens, or connection strings into
  code, docs, commits, or logs. Use environment variables or a secrets manager.
- NEVER read, open, or echo `.env`, `.env.*`, `secrets/**`, credential files,
  or `.git/config`. (Enforced by deny-rules + `secret-scan.sh` PreToolUse hook.)

## Article 2 — Production data is read-only by default (HARD)
- Treat all client/production databases (SQL Server, Azure SQL, Power BI models)
  as READ-ONLY. No `INSERT` / `UPDATE` / `DELETE` / `DROP` / `ALTER` / `EXEC` /
  `GRANT` unless Sergio explicitly authorizes a specific write, in writing, for a
  specific task. (Enforced by `sql-guard.sh` PreToolUse hook + read-only MCP.)
- Prefer a read-only MCP connection (`ApplicationIntent=ReadOnly`, `db_datareader`).

## Article 3 — Financial-information redaction (HARD)
- Do NOT retain, summarize into memory, or reproduce Sergio's personal financial
  information unless explicitly instructed for the current task.
- Do not persist client financial figures into `MEMORY.md` or auto-memory.

## Article 4 — Evidence over assumption
- Do not assume a project's stack, schema, or conventions. Read its `CLAUDE.md`
  and `docs/` first. State assumptions explicitly when unavoidable.
- Verify by running: prefer executing tests/queries over claiming success.

## Article 5 — Document before building
- PRD before any feature. ADR before any architectural decision.
- If either is missing, create or propose it first and get approval before coding.

## Article 6 — Handoff discipline
- Subagents run in isolated context and return a summary to the main thread.
- Subagents do not call each other; the main thread chains specialists.
- Each delegation must include: objective, output format, allowed tools, and
  explicit boundaries ("do not do X").
- Routing: the main thread picks the specialist per the routing table in
  `docs/agents/ORCHESTRATION.md` (task → agent). With no clear owner, default to
  the closest-scope agent and state the choice.

## Article 7 — Language & artifacts
- Converse with Sergio in Spanish; explain technical concepts pedagogically even
  when unprompted, defining terms as they appear.
- All code, docs, PRDs, ADRs, commit messages, and config remain in English.
- Commit messages: descriptive, conventional-commits style, in English.

## Article 8 — Tool-matrix citation (HARD wording)
- When citing the tool matrix, use verbatim:
  "Según la matriz de herramientas (v.20 mayo 2026):"

## Article 9 — Scope & least privilege
- Read-only / reviewer agents must not have `Edit` / `Write` / `Bash`.
- Do not edit locked design artifacts (e.g., Kibo `decisions.json`).
- Prefer the smallest model that fits the task (Haiku for search, Sonnet for
  build, Opus for coordination / judgment).

## Amendments
- This file is versioned. Changes require a Sync Impact note (date + what changed).
- Project-level constitutions may add stricter articles; they may never weaken these.

<!-- Sync Impact log
  v1.1 (2026-06-23): Article 6 — added a routing clause (the main thread routes
  task->agent per docs/agents/ORCHESTRATION.md; defaults to the closest-scope agent
  when no clear owner exists).
  v1.0 (2026-06-20): Initial constitution. Consolidates rules previously scattered
  across root CLAUDE.md and per-project CLAUDE.md files.
-->
