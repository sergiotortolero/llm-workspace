# LLM Workspace — Orquestador General

Workspace de orquestación para proyectos creados con IA (Claude Code).
Mapa completo en [WORKSPACE.md](WORKSPACE.md) · reglas en [CLAUDE.md](CLAUDE.md).

> **Repo privado.** Incluye contexto de proyectos personales y de trabajo (TIBS).
> **No** incluye secretos (`.env`), binarios, datos de dispositivos ni dumps de BD
> (ver `.gitignore`). Propósito: dar contexto a herramientas de IA (Claude, Gemini) para
> investigación y soporte.

## Estructura
- `.claude/` — agentes, comandos y configuración de Claude Code.
- `docs/` — `agents/` (catálogo + orquestación), `context/` (perfil + onboarding), `adr/`, `setup/`.
- `templates/`, `scripts/` — plantillas y utilidades de scaffolding.
- `Proyectos/TIBS/` — proyectos de trabajo (6 iniciativas). `Proyectos/Personal/` — personales.

## Nota
**Kibo** vive en su propio repositorio: `github.com/kibo-developer/kibo-platform`
(no se incluye aquí para no duplicar ni romper su historial).
