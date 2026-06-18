---
description: Scaffold a new project folder with the standard docs structure (prd/adr/audits) and seed shared templates
argument-hint: <ProjectName>
allowed-tools: Bash, Write
---
Create the standard project structure for "$1".

Steps:
1. If `D:\LLM's\Proyectos\$1` does not exist, create it.
2. Run `scripts\New-ProjectDocs.ps1 -ProjectName "$1"` to create `docs/prd`, `docs/adr`, `docs/audits` and seed the templates.
3. Create a starter `Proyectos\$1\CLAUDE.md` capturing: one-line purpose, target users, and a "stack: TBD — pending ADR" note.
4. Report the created paths and remind Sergio that a PRD is required before building any feature.
