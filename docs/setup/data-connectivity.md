# Setup — Conexión a SQL y Power BI (MCP)

Guía para conectar Claude Code a la base de datos detrás de Power BI y a los semantic
models. El objetivo: analizar/auditar stored procedures y generar la versión
"white-level". **Empezamos por la estructura; la conexión en vivo se afina después.**

## Conceptos rápidos (para PM)
- **MCP (Model Context Protocol):** estándar que deja que un agente de IA use herramientas
  externas (p. ej. consultar tu base de datos) de forma controlada y segura.
- **Stored Procedure (SP):** lógica SQL guardada *dentro de la base de datos*, no en Power
  BI. Por eso auditar "los SP de Power BI" = auditar la **base de datos** que lo alimenta.
- **XMLA endpoint:** la "puerta" para conectar herramientas al semantic model de Power BI.
  Solo disponible en workspaces **Premium / PPU / Fabric**.

## Opción A — SQL MCP Server (recomendada para los SP)
Servidor oficial de Microsoft sobre **Data API Builder**. Lista objetos, lee datos y
**ejecuta stored procedures**.

1. Instala la herramienta: `dotnet tool install -g Microsoft.DataApiBuilder`
2. Crea `dab-config.json` apuntando a tu base con tu *connection string*.
3. Expón el endpoint MCP y registra el servidor en `.mcp.json` (ver `.mcp.json.example`).
4. Docs: https://learn.microsoft.com/en-us/sql/mcp/ ·
   https://devblogs.microsoft.com/azure-sql/introducing-sql-mcp-server/

## Opción B — Power BI MCP (semantic models)
- **Local / Modeling:** `https://github.com/microsoft/powerbi-modeling-mcp` — lee y escribe
  TMDL en una carpeta PBIP (ideal para versionar el modelo en git).
- **Remoto:** consulta el modelo con DAX en lenguaje natural. Requiere XMLA (Premium/PPU/Fabric).
  https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started
- Overview: https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview

## Opción C — Scripts read-only (sin MCP, fallback)
Si todavía no instalamos MCP, el agente `data-platform` puede generar scripts de solo
lectura (`sqlcmd` o Python con `pyodbc`/`pymssql`) para que tú los ejecutes. Nunca se
guardan credenciales en archivos: van por variables de entorno.

## Lo que necesito de Sergio para conectar de verdad
1. **Motor y hosting:** ¿SQL Server on-prem, Azure SQL, u otro?
2. **Connection string / credenciales** (o cómo accedes hoy).
3. **Power BI:** ¿el workspace es Premium / PPU / Fabric? (define si hay XMLA).
4. **"White-level":** qué significa exactamente el entregable (ver ADR 0002).
5. **Permisos:** ¿solo lectura para auditar, o también necesitarás escribir?

> Seguridad: por defecto trabajamos en **solo lectura**. Cualquier escritura/DDL se
> confirma explícitamente. No se commitea ningún secreto al repositorio.

## Cómo descubrir el motor y el tier (guía para PM, sin tecnicismos)

### 1) ¿Qué motor/hosting es la base de datos?
Desde **Power BI Desktop**, con tu reporte abierto:
1. Pestaña **Inicio (Home)** → **Transformar datos (Transform data)** → **Configuración del
   origen de datos (Data source settings)**.
2. Ahí verás el **nombre del servidor** y la **base de datos**. Pásamelo (o una captura).
3. Cómo leerlo:
   - Termina en **`.database.windows.net`** → es **Azure SQL** (nube).
   - Es un nombre de servidor o IP normal (p. ej. `SRV-DATOS\SQL2019`) → **SQL Server on-prem**.
   - Dice `postgres`/`mysql` en el conector → otro motor.

> No necesito tu contraseña para esto: con el nombre del servidor y la base ya sé cómo
> armar la conexión. Las credenciales se manejan aparte y nunca se guardan en archivos.

### 2) ¿Qué tier de Power BI tienes? (define si hay XMLA)
En **Power BI Service** (https://app.powerbi.com):
1. Mira tus **workspaces** en el panel izquierdo. Si junto al nombre hay un **ícono de
   diamante 💎** → es **Premium / Fabric** (hay XMLA, podemos usar el MCP de Power BI).
2. Si no hay diamante → probablemente **Pro/estándar** (sin XMLA): nos enfocamos en la
   base de datos SQL, que es donde están los stored procedures de todos modos.
3. Si quieres confirmar la licencia: ícono de tu **perfil** (arriba a la derecha) →
   muestra el tipo de licencia.

> Para tu objetivo (auditar y generar el **white-label** de los stored procedures), lo
> crítico es la **conexión SQL**, no el tier de Power BI. El XMLA solo importa si además
> quieres tocar el modelo semántico.

## White-level = white-label (decidido)
El entregable es una versión **neutral/genérica**: catalogar cada objeto, marcar la lógica
propietaria o específica de cliente (nombres, valores hardcodeados, reglas particulares) y
producir la versión abstraída + un mapa de qué se generalizó. Detalle en `docs/adr/0002`.
