# Orquestador General — Sergio Tortolero

@constitution.md
<!-- ^ Imports the global immutable laws (security, read-only DB, financial redaction,
     evidence, PRD/ADR, handoff, language, tool-matrix, least-privilege).
     Keep the rules there — do NOT duplicate them in this file. -->

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
- Seguimiento Chubb (Alteryx, Siniestralidad, Enlace Chile) — solo seguimiento (contacto Chubb, quincenal)
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

## Reglas globales → constitución
Las leyes inmutables viven en `constitution.md` (importada arriba con `@constitution.md`).
No se duplican aquí; este es solo el mapa de dónde quedó cada una:
- Idioma y explicar conceptos → Art. 7 · Commits descriptivos en inglés → Art. 7
- PRD antes de feature · ADR antes de arquitectura → Art. 5
- No asumir el stack sin leer el `CLAUDE.md` del proyecto → Art. 4
- No retener información financiera → Art. 3
- Cita exacta de la matriz de herramientas → Art. 8
- (Refuerzos nuevos) Secretos fuera del código → Art. 1 · Datos de producción read-only → Art. 2

## Skills disponibles globalmente
prompt-optimizer, senior-architect, senior-fullstack, senior-frontend,
senior-backend, senior-qa, agile-product-owner, ui-designer,
tech-stack-evaluator, competitors-analysis, deep-research,
ux-researcher-designer, code-reviewer, senior-devops, cloud-security

## Cómo orquesto los proyectos
Desde esta carpeta raíz superviso todos los proyectos. Para trabajar
en uno específico me muevo a su carpeta y abro Claude Code ahí.

## Agentes
Invoca: "usa el agente <nombre> para ...". Hay **tres ubicaciones** (importa por cómo
Claude Code los descubre: sube por el árbol pero se detiene en el `.git` más cercano).

**Transversales — en `~/.claude/agents/` (user scope, GLOBALES de verdad).**
Disponibles en CUALQUIER carpeta y proyecto, incluso repos con su propio `.git` (ej. Kibo).
- `product-planner` → planeación, roadmap, backlog, sprints, estimación, priorización.
- `ux-researcher` → investigación UX, personas, journey maps, usabilidad.
- `ui-designer` → diseño visual/UI, design systems, tokens, branding.
- `solution-architect` → arquitectura, ADRs, evaluación de stack, diagramas.
- `security-auditor` → revisiones de seguridad, threat modeling, cloud/app security.
- `qa-engineer` → estrategia y generación de pruebas, calidad.
- `code-reviewer` → revisión de código (calidad, correctitud, seguridad).
- `devops-engineer` → Docker, CI/CD (GitHub Actions), pnpm/Turbo, envs/secrets, despliegue.
- `data-engineer` → ETL/Postgres/telemetría IoT/Streamlit data apps (complementa a data-platform).
- `python-pro` → código Python idiomático y type-safe, pytest, pandas/NumPy, Streamlit/Postgres.
- `business-analyst` → análisis de negocio/mercado/competencia, business cases, requisitos.
- `technical-writer` → documentación técnica (READMEs, arquitectura, API, traducción).
- `ai-engineer` → features con LLM (prompts, RAG, evals, integración de la API de Claude).

**De dominio — en `D:\LLM's\.claude\agents\` (workspace; visibles en todos los proyectos
EXCEPTO en repos con `.git` propio como Kibo).**
- `pm-docs` → minutas, status reports, PRDs, historias, comunicación interna.
- `data-platform` → SQL Server + Power BI: conexión/análisis/auditoría, entregable white-label.
- `web-architect` → construcción de plataformas web (Kibo, Mouna).

**De proyecto — en `<proyecto>/.claude/agents/`.** Ej. `streamlit-migrator` (PMR),
`requirements-agent` (Kibo). Se activan al abrir Claude Code dentro de esa carpeta.

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