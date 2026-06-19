# Orquestación de agentes

Cómo el **agente maestro** (el orquestador en la raíz `D:\LLM's`) coordina a los subagentes
para tener una estructura general bien organizada.

## Principio (realidad de Claude Code)
- Los subagentes corren en **contexto aislado** y **devuelven** su resultado al maestro.
- **No se invocan entre sí.** Quien encadena especialistas es el **maestro** (hilo principal).
- Por eso "que un agente llame a otro" se implementa como: el maestro llama a A, lee su
  salida, y con eso llama a B. Cada agente **recomienda** el siguiente (handoff), pero el
  maestro ejecuta la cadena.

## Roster
Ubicación importa (descubrimiento sube por el árbol hasta el `.git` más cercano):
- **Transversales — `~/.claude/agents/` (user scope, globales de verdad):** `product-planner`,
  `ux-researcher`, `ui-designer`, `solution-architect`, `security-auditor`, `qa-engineer`,
  `code-reviewer`, `devops-engineer`, `data-engineer`, `python-pro`, `business-analyst`,
  `technical-writer`, `ai-engineer`.
- **De dominio — `D:\LLM's\.claude\agents\` (workspace; no llegan a repos con `.git` propio):**
  `pm-docs`, `data-platform`, `web-architect`.
- **De proyecto — `<proyecto>/.claude/agents/`:** p. ej. `streamlit-migrator` (PMR),
  `requirements-agent` (Kibo). Activos al abrir Claude Code en su carpeta.

## Tabla de ruteo (tarea → agente)
| Necesito… | Agente |
|---|---|
| Minuta / status / PRD / comunicación | `pm-docs` |
| Documentación técnica / README / traducción | `technical-writer` |
| Roadmap / backlog / sprint / estimación | `product-planner` |
| Análisis de negocio / mercado / competencia / business case | `business-analyst` |
| Investigación de usuarios / journeys | `ux-researcher` |
| Diseño visual / design system / branding | `ui-designer` |
| Decisión de arquitectura / stack / ADR | `solution-architect` |
| Construir web (Kibo/Mouna) | `web-architect` |
| SQL Server / Power BI / auditoría de datos | `data-platform` |
| ETL / Postgres / telemetría IoT / Streamlit data app | `data-engineer` |
| Código Python (módulos, refactor, pytest, pandas) | `python-pro` |
| Docker / CI/CD / despliegue / envs | `devops-engineer` |
| Feature con LLM (prompts/RAG/evals/API Claude) | `ai-engineer` |
| Revisión de seguridad / secretos / cloud | `security-auditor` |
| Estrategia y generación de pruebas | `qa-engineer` |
| Revisión de código (PR/diff) | `code-reviewer` |
| Migrar PMR React→Streamlit | `streamlit-migrator` (en su carpeta) |

## Cadenas típicas (el maestro las ejecuta en orden)
- **Feature nueva (web):** `product-planner` → `ux-researcher` → `ui-designer` →
  `solution-architect` → `web-architect` → `qa-engineer` → `code-reviewer` → `security-auditor`.
- **Proyecto de datos:** `solution-architect` → `data-platform` → `security-auditor` (secretos/acceso) → `code-reviewer`.
- **Migración PMR:** `solution-architect` (decisiones) → `streamlit-migrator` (build por fases) → `qa-engineer` → `security-auditor` (auth).
- **Revisión previa a entregar:** `code-reviewer` + `security-auditor` + `qa-engineer`.

## Cómo lo pides
- Un agente: *"usa el agente `ui-designer` para definir los tokens de Mouna"*.
- Una cadena: *"coordina: planea, valida UX, diseña y propón arquitectura para X"* — yo ejecuto
  la secuencia y te traigo el resultado consolidado.

## Personalización
Cada agente sigue tus reglas (español en conversación; código/docs en inglés; PRD antes de
features; ADR antes de arquitectura; explicar conceptos; no retener info financiera) y apunta
a las **skills** de Anthropic correspondientes. Catálogo de agentes externos: `AGENT-CATALOG.md`.
