# APPLY-CHANGES — Instrucciones para el agente (Claude Code)

<!--
  Sergio adjunta este archivo + los demás en el chat de Claude Code.
  Este archivo es el ÍNDICE y las INSTRUCCIONES de colocación. El agente debe
  leerlo primero y seguirlo al pie de la letra.
  Abrir Claude Code en la RAÍZ del workspace (D:\LLM's), no dentro de Kibo.
-->

Sergio te adjunta varios archivos en el chat. Tu trabajo es colocarlos en su
ubicación correcta dentro del workspace `D:\LLM's`, referenciarlos donde
corresponda, y dejar todo funcionando. Explícale en español cada concepto que
toques (está aprendiendo); todo archivo/código/config queda en inglés.

## Regla de oro antes de ejecutar
Para cualquier cambio sobre `settings.json`, hooks o deny rules: **muestra el diff
y espera aprobación explícita de Sergio.** Los archivos nuevos (`constitution.md`,
docs, scripts) puedes crearlos ya, pero NO actives los hooks en `settings.json`
hasta que Sergio apruebe el diff. Si algo de estos archivos contradice el estado
real del workspace, gana el workspace real: avísale de la discrepancia.

## Paso 0 — Validación
1. Lee el `CLAUDE.md` raíz, `WORKSPACE.md`, `docs/agents/ORCHESTRATION.md`.
2. Corre `/memory` y reporta qué CLAUDE.md y agentes se cargan ahora.
3. Confirma qué se cargaría si Claude Code se abre dentro de Kibo (su propio `.git`).

## Paso 1 — Colocar los archivos adjuntos

| Archivo adjunto             | Colocar en (ruta exacta)                  | Acción |
|-----------------------------|-------------------------------------------|--------|
| `constitution.md`           | `D:\LLM's\constitution.md` (raíz)         | Crear  |
| `enforcement-config.md`     | `docs/setup/enforcement-config.md`        | Crear  |
| `secret-scan.sh`            | `.claude/hooks/secret-scan.sh`            | Crear + `chmod +x` |
| `sql-guard.sh`              | `.claude/hooks/sql-guard.sh`              | Crear + `chmod +x` |
| `APPLY-CHANGES.md` (este)   | `docs/agents/APPLY-CHANGES.md` (archivo)  | Guardar como bitácora |

## Paso 2 — Referenciar la constitución desde el CLAUDE.md raíz
Añade al `CLAUDE.md` raíz, cerca del inicio, la línea de import nativa:

```
@constitution.md
```

Esto carga la constitución automáticamente en cada sesión. Luego **mueve** a
`constitution.md` las reglas que hoy están dispersas en el `CLAUDE.md` raíz
(idioma, PRD/ADR, no-financiero, cita de la matriz de herramientas) para que el
CLAUDE.md quede más delgado (solo "sustantivos": qué/dónde, proyectos, rutas).
Muéstrame qué quitaste y de dónde. No dupliques: si una regla ya vive en la
constitución, en CLAUDE.md déjala solo como referencia, no repetida.

## Paso 3 — Enforcement determinista (REQUIERE APROBACIÓN)
Sigue `docs/setup/enforcement-config.md`:
- Añade las `deny` rules a `~/.claude/settings.json` (user scope, MERGE — no
  borres claves existentes).
- Registra los hooks en `.claude/settings.json` (workspace scope).
- Explícame línea por línea qué hace cada script y por qué `exit 2` bloquea.
- Muéstrame el diff de ambos `settings.json` y ESPERA mi "ok" antes de escribir.

## Paso 4 — Verificación
Corre el mini smoke test de la sección 3 de `enforcement-config.md` (secret-scan,
sql-guard, y un control negativo que debe pasar). Reporta resultados.

## Paso 5 — Cierre
Dame un resumen: qué creaste, qué moviste y de dónde, qué quedó pendiente de mi
aprobación, y el resultado del smoke test. NO toques agentes del roster ni el
diseño del plugin en esta corrida — eso lo haremos en una sesión aparte.
