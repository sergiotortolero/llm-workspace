# Workspace — Orquestador General

Este es el **nivel raíz de orquestación**. Desde aquí Sergio (PM) supervisa todos los
proyectos. Cada proyecto vive en `Proyectos/<Nombre>` y tiene su propio `CLAUDE.md`,
stack y documentación. Este nivel define **convenciones compartidas** y plantillas
reutilizables, no código de producto.

> Reglas de idioma: conversación y explicaciones en **español**; código, commits y
> documentación técnica en **inglés**. (Ver `CLAUDE.md` y `.claude/spanish.md`.)

## Estructura

```
D:\LLM's\
├── CLAUDE.md              # Reglas globales del orquestador (no tocar sin razón)
├── WORKSPACE.md           # Este archivo: mapa y convenciones
├── templates/             # Plantillas reutilizables (se copian a cada proyecto)
│   ├── prd-template.md
│   ├── adr-template.md
│   ├── user-story-template.md
│   └── db-audit-template.md
├── scripts/               # Utilidades de orquestación (PowerShell)
│   └── New-ProjectDocs.ps1
├── docs/                  # Documentación a nivel orquestador (decisiones cross-proyecto)
│   ├── prd/
│   └── adr/
└── Proyectos/
    ├── TIBS/                   # Trabajo — CLAUDE.md compartido (clientes, stakeholders)
    │   ├── Guarda Express/                      # BI — cliente (Power BI consolidación financiera)
    │   ├── Tablero de Consolidación Financiera/ # BI — interno (antes Data-SQL-PowerBI)
    │   ├── Seguimiento Chubb/                   # BI — solo seguimiento (contacto Chubb, quincenal)
    │   ├── Corrections Module PMR - Streamlit/  # Desarrollo — Chubb (React→Streamlit) 🔴 urgente
    │   ├── WebMethods - XPD Global/             # Desarrollo — SAP B1 ↔ CargoWise (asesoría, en cierre)
    │   └── AppConsulta/                         # Desarrollo — utilitario local (solo referencia)
    └── Personal/               # Personales — CLAUDE.md compartido
        ├── Kibo/                               # Personal OS gamificado/RPG (React)
        ├── Mouna/                              # Web de colectivo de arte (ShadCN)
        └── Shelly - Censo de Cargas/          # Telemetría Shelly Pro 3EM (Postgres + Streamlit)
```

> Estructura (2026-06-18): proyectos agrupados en **TIBS/** (6 iniciativas) y **Personal/** (3),
> cada uno con `CLAUDE.md` de contexto compartido heredable. Todos los proyectos tienen `docs/`
> (prd/adr/audits). Mover los repos con Docker (Kibo, Shelly) fue seguro: usan rutas relativas.

## Flujo de trabajo (de PM a build)

1. **Idea → PRD.** Antes de construir cualquier feature, debe existir un PRD en
   `docs/prd/` del proyecto. Usa `templates/prd-template.md`.
2. **Decisión técnica → ADR.** Antes de fijar arquitectura, crea un ADR en
   `docs/adr/` del proyecto. Usa `templates/adr-template.md`.
3. **PRD → Historias.** Desglosa el PRD en historias con `templates/user-story-template.md`.
4. **Build.** Trabaja dentro de la carpeta del proyecto; abre Claude Code ahí para
   heredar su `CLAUDE.md` y stack.

## Convención de carpetas por proyecto

Todo proyecto debería tener como mínimo:

```
Proyectos/<Nombre>/
├── CLAUDE.md          # Stack, reglas y contexto del proyecto
├── docs/
│   ├── prd/           # Product Requirements Documents
│   ├── adr/           # Architecture Decision Records
│   └── audits/        # Auditorías (DB, seguridad, performance)
└── ...código...
```

Para crear esa estructura en un proyecto nuevo:

```powershell
.\scripts\New-ProjectDocs.ps1 -ProjectName "Kibo"
```

## Conectores / MCP

Estado actual: **0 conectores instalados**. Para tareas de datos (auditar la base de
datos detrás de PowerBI, leer Stored Procedures) hace falta conectar un MCP de SQL
Server o trabajar con scripts directos. Ver `docs/adr/` para la decisión registrada.
