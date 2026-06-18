---
description: Process the context inbox — read raw dumps and distill them into memory, CLAUDE.md, about-me, and project docs
allowed-tools: Read, Write, Edit, Glob, Grep
---
Process Sergio's context intake.

1. List and read every file in `docs/context/inbox/` (ignore its `README.md`).
2. For each piece of information, decide where it belongs:
   - Durable atomic fact (who he is, a goal, a decision) → a **memory** file (+ MEMORY.md index entry).
   - A rule/instruction Claude must always follow → the relevant **CLAUDE.md** (root or project).
   - Long-form profile/business context → `docs/context/about-me.md` or `business-and-goals.md`.
   - Project-specific background → that project's `docs/` (PRD, or a context doc).
3. Ask Sergio about anything ambiguous or conflicting BEFORE writing.
4. Never store secrets (passwords, tokens, connection strings). Flag them if found.
5. After distilling, show a summary table: what was saved and where, and what was skipped/needs clarification.
6. Tell Sergio he can now archive or delete the processed raw files in the inbox.

Respond in Spanish.
