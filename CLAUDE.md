# Orquestador General — Sergio Tortolero

## Quién soy
PM aprendiendo vibe coding. Sin rol técnico pero con criterio 
para evaluar decisiones. Creo productos digitales con IA, aprendiendo "vibe coding".
Product Manager en TIBS (consultora de datos en Monterrey; clientes: Chubb, GCC,
Prolamsa, XPD Global; lidero 6 iniciativas). Ex Scrum Master (Grupo Salinas, Santander).
Herramientas: Claude Pro/Max, Gemini Advanced, NotebookLM.
Perfil completo en docs/context/about-me.md y en la memoria.

## Proyectos activos
Agrupados en dos carpetas con CLAUDE.md de contexto compartido.

### Trabajo — TIBS (Proyectos/TIBS/) — 6 iniciativas
BI (líder Abel Martínez):
- Guarda Express (cliente; Power BI de consolidación financiera)
- Tablero de Consolidación Financiera (interno; antes "Data-SQL-PowerBI")
- Seguimiento Chubb (Alteryx, Siniestralidad, Enlace Chile) — solo seguimiento (Sara Torres, quincenal)
Desarrollo (líder Héctor Esparza):
- Corrections Module PMR - Streamlit (Chubb) — 🔴 PRIORIDAD ACTUAL
- WebMethods - XPD Global (SAP B1 ↔ CargoWise) — asesoría, en cierre
- AppConsulta (app vive fuera; utilitario local = solo referencia)

### Personales (Proyectos/Personal/)
- Kibo (Personal OS gamificado/RPG, React; prioridad personal)
- Mouna (web de colectivo de arte con amigos; ShadCN)
- Shelly - Censo de Cargas (telemetría Shelly Pro 3EM; Postgres+Streamlit)

Stakeholders TIBS: Mario Monroy (Dir. General) · Abel Martínez (BI) · Héctor Esparza
(Desarrollo) · Chubb: Liliana Pérez (líder directa) → Marcio Bueno (Data LATAM).
Contexto: Proyectos/TIBS/CLAUDE.md y Proyectos/Personal/CLAUDE.md.

## Reglas globales
- Respóndeme en español, código y docs en inglés
- Explícame conceptos técnicos aunque no te los pida
- Antes de construir cualquier feature: verifica que existe PRD en docs/prd/
- Antes de decidir arquitectura: crea ADR en docs/adr/
- No asumas el stack de ningún proyecto sin leer su CLAUDE.md
- Commits descriptivos en inglés explicando qué se hizo y por qué
- No retengas información financiera de Sergio salvo instrucción explícita suya
- Al citar la matriz de herramientas: "Según la matriz de herramientas (v.20 mayo 2026):"

## Skills disponibles globalmente
prompt-optimizer, senior-architect, senior-fullstack, senior-frontend,
senior-backend, senior-qa, agile-product-owner, ui-designer,
tech-stack-evaluator, competitors-analysis, deep-research,
ux-researcher-designer, code-reviewer, senior-devops, cloud-security

## Cómo orquesto los proyectos
Desde esta carpeta raíz superviso todos los proyectos. Para trabajar
en uno específico me muevo a su carpeta y abro Claude Code ahí.

## Agentes (subagentes en .claude/agents/)
Globales: sirven en TODOS los proyectos. Invoca: "usa el agente <nombre> para ...".

De dominio:
- `pm-docs` → minutas, status reports, PRDs, historias, comunicación interna.
- `data-platform` → SQL + Power BI: conexión/análisis/auditoría, entregable white-label.
- `web-architect` → construcción de plataformas web (Kibo, Mouna).

Transversales (mejores prácticas, cualquier proyecto):
- `product-planner` → planeación, roadmap, backlog, sprints, estimación, priorización.
- `ux-researcher` → investigación UX, personas, journey maps, usabilidad.
- `ui-designer` → diseño visual/UI, design systems, tokens, branding.
- `solution-architect` → arquitectura, ADRs, evaluación de stack, diagramas.
- `security-auditor` → revisiones de seguridad, threat modeling, cloud/app security.
- `qa-engineer` → estrategia y generación de pruebas, calidad.
- `code-reviewer` → revisión de código (calidad, correctitud, seguridad).

A nivel proyecto puede haber agentes propios (ej. `streamlit-migrator` en el PMR) que se
activan al abrir Claude Code dentro de esa carpeta.

### Orquestación
Para tareas complejas, pídeme coordinar varios en cadena (ej.: producto nuevo →
`product-planner` → `ux-researcher` → `ui-designer` → `solution-architect` → construcción →
`qa-engineer` → `code-reviewer` → `security-auditor`). El agente maestro (hilo principal)
coordina; cada subagente trabaja aislado y devuelve su resultado (no se llaman entre sí).
Mapa completo: `docs/agents/ORCHESTRATION.md`.

## Comandos (.claude/commands/)
- `/new-project <Nombre>` → crea carpeta + estructura docs (prd/adr/audits).
- `/minuta <notas>` → genera una minuta en español (vía pm-docs).
- `/audit-db [scope]` → corre la auditoría de base de datos (vía data-platform).
- `/status` → resumen del estado de todos los proyectos.

## Conectores (MCP) — datos
Plantilla en `.mcp.json.example`; guía en `docs/setup/data-connectivity.md`.
Servidores oficiales de Microsoft: SQL MCP Server (ejecuta stored procedures) y
Power BI MCP (remoto + modelado local). Decisión pendiente en `docs/adr/0002`.

## Memoria
Hechos durables en la carpeta de memoria de Claude (índice: MEMORY.md). No duplicar
lo que ya vive en este CLAUDE.md o en el código.

## Plantillas y scripts
- `templates/` → prd, adr, user-story, db-audit.
- `scripts/New-ProjectDocs.ps1` → scaffolding de docs por proyecto.
- Mapa general del workspace: `WORKSPACE.md`.