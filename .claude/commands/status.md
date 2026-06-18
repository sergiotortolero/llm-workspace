---
description: Summarize the status of all active projects from the orchestrator root
allowed-tools: Read, Glob, Grep
---
Give Sergio a concise status overview across all projects under `D:\LLM's\Proyectos`.

For each project:
- Read its `CLAUDE.md` (if present) for purpose and stack.
- Check `docs/prd`, `docs/adr`, `docs/audits` for what exists.
- Report: project name, one-line purpose, stack (or "TBD"), and what artifacts/docs exist vs. are missing.

Finish with a short prioritized list of suggested next actions (Kibo is the stated current priority). Keep it scannable — a table is ideal.
