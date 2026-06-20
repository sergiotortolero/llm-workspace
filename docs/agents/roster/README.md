# Roster de agentes generales (respaldo versionado)

Copia **versionada** de los agentes *user scope* que viven en `~/.claude/agents/` (fuera del
workspace, para ser globales en TODOS los proyectos, incluso repos con su propio `.git`).
Se respaldan aquí para no perderlos y para que **otras IAs puedan auditar la estructura**.

> Para desplegarlos en una máquina nueva: copia estos `.md` a `~/.claude/agents/`.

## Contenido (13 transversales)
`product-planner`, `ux-researcher`, `ui-designer`, `solution-architect`, `security-auditor`,
`qa-engineer`, `code-reviewer`, `devops-engineer`, `data-engineer`, `python-pro`,
`business-analyst`, `technical-writer`, `ai-engineer`.

Los agentes **de dominio** (`pm-docs`, `data-platform`, `web-architect`) viven en
`.claude/agents/`. Los **de proyecto** viven en `<proyecto>/.claude/agents/`.

Modelo de orquestación y tabla de ruteo: ver [`../ORCHESTRATION.md`](../ORCHESTRATION.md)
y [`../AGENT-CATALOG.md`](../AGENT-CATALOG.md).
