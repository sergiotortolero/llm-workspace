# Catálogo de agentes — investigado y mapeado a tus proyectos

Investigación (jun 2026) de los agentes/subagentes disponibles para Claude Code, filtrados
según tu perfil (PM "vibe coding") y tus 6 proyectos. **Recomendación clave: NO instales
150 agentes de golpe** — generan ruido. Curamos ~10–12 que calzan con tu stack.

## Fuentes principales
- **Oficial de Anthropic** — directorio gestionado: https://github.com/anthropics/claude-plugins-official
- **VoltAgent/awesome-claude-code-subagents** (154+ agentes en 10 categorías):
  https://github.com/VoltAgent/awesome-claude-code-subagents
- **wshobson/agents** (marketplace multi-harness, ~37k★): https://github.com/wshobson/agents
- **0xfurai/claude-code-subagents** (100+): https://github.com/0xfurai/claude-code-subagents
- **Directorio de marketplaces/plugins:** https://claudemarketplaces.com/
- Docs oficiales de plugins: https://code.claude.com/docs/en/plugins

> Ya tienes activo el set de **anthropic-skills** (senior-architect, senior-fullstack,
> senior-frontend/backend, senior-qa, agile-product-owner, ui-designer, cloud-security,
> code-reviewer, deep-research, etc.) y skills de **data** (sql-queries, build-dashboard…).
> Mucho de lo que necesitas YA está cubierto por skills; los subagentes externos son para
> llenar huecos puntuales.

## Mapa: proyecto/rubro → agente recomendado

| Tu rubro / proyecto | Necesidad | Recomendado | De dónde |
|---|---|---|---|
| **PM / minutas** (pm-docs) | Product/PM, análisis de negocio | `product-manager`, `business-analyst` | VoltAgent `08-business-product` + skill `agile-product-owner` (ya lo tienes) |
| **Kibo / Mouna** (web-architect) | Fullstack, frontend, backend | `fullstack-developer`, `frontend-developer`, `backend-developer` | VoltAgent `01-core-development` + skills senior-* (ya) |
| **Tablero de Consolidación Financiera** (data-platform) | Data engineering, SQL, BI | `data-engineer`, `sql-pro` | VoltAgent `05-data-ai` + skills `sql-queries`/`build-dashboard` (ya) |
| **React-to-Streamlit / Shelly** | Python, Streamlit, datos | `python-pro`, `data-engineer` | VoltAgent / 0xfurai (no hay uno "Streamlit" dedicado — se cubre con python-pro) |
| **Shelly / Kibo** | Docker, despliegue, IoT | `devops-engineer`, `deployment-engineer` | VoltAgent `04-devops` + skill `senior-devops` (ya) |
| **AppConsulta** | iOS / mobile, scripting | `mobile-developer` | VoltAgent `01-core-development` |
| **Transversal** | QA, seguridad, code review | `qa-expert`, `security-auditor`, `code-reviewer` | VoltAgent + skills (ya) |

## Cómo instalar (3 vías, de más simple a más manual)

1. **Marketplace de plugins (recomendado).** En tu terminal de Claude Code corre `/plugin`,
   agrega un marketplace (ej. el oficial o `wshobson/agents`) y elige instalar a **scope de
   usuario** (`~/.claude/`, vale para todos los proyectos) o **de proyecto** (`.claude/`).
   *(Este comando es interactivo; lo corres tú en la terminal — yo no puedo abrirlo.)*
2. **Copiar subagentes sueltos.** De repos como VoltAgent/0xfurai, tomar el `.md` de un
   agente y colocarlo en `~/.claude/agents/` (global) o en `<proyecto>/.claude/agents/`.
   **Yo sí puedo hacer esto por ti** si me dices cuáles quieres (los traigo y los adapto).
3. **Adaptar, no copiar tal cual.** Lo mejor es tomar el agente externo como base y
   ajustarlo a tus reglas (idioma, PRD/ADR primero, etc.) — como hicimos con tus 3 actuales.

## Recomendación de arranque (shortlist curada)
Para no saturar, empezaría con estos, adaptados a tu workspace:
- Mantener tus 3 actuales (`pm-docs`, `data-platform`, `web-architect`).
- Añadir cuando los necesites: `qa-expert`, `security-auditor`, `devops-engineer`,
  `mobile-developer` (para AppConsulta).
- El resto (frontend/backend/python/data) ya está cubierto por las **skills** que tienes.

> Próximo paso sugerido: tú eliges de la tabla cuáles quieres y yo los doy de alta
> (vía 2/3) adaptados a tus reglas. Primero conviene cargar tu contexto (ver `docs/context/`)
> para personalizarlos bien.
