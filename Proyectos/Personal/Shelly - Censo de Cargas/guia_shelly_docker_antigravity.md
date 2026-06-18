# Guía técnica para exportación, almacenamiento y corrección de datos del Shelly Pro 3EM

## Objetivo

Implementar una solución local basada en Docker para:

1. Extraer mediciones del Shelly Pro 3EM mediante un script JavaScript ejecutado en el propio dispositivo.
2. Recibir y persistir la telemetría en una base de datos relacional dentro de Docker.
3. Mantener una tabla **raw** (cruda) sin alterar.
4. Corregir posteriormente periodos contaminados:
   - fase B sin referencia de voltaje,
   - CT invertido en una fase,
   - otros incidentes documentados.
5. Generar un ejecutable `.exe` que actualice las correcciones sobre la base cruda o materialice una capa curada para análisis.
6. Dejar documentado un prompt para que un agente técnico de Antigravity implemente el stack completo.

---

## Arquitectura propuesta

### Componentes

- **Shelly Pro 3EM**
  - Ejecuta un script JavaScript interno.
  - Consulta su propio estado mediante RPC `EM.GetStatus`.
  - Envía un `HTTP POST` cada 60 segundos al receptor local.

- **Servicio receptor local**
  - Corre en Docker.
  - Expone una API HTTP simple.
  - Recibe JSON del Shelly y lo inserta en base de datos.

- **Base de datos en Docker**
  - Recomendación: **PostgreSQL**.
  - Ventajas:
    - soporte robusto para SQL, vistas, funciones y procedimientos,
    - fácil de contenerizar,
    - buena compatibilidad con herramientas de BI,
    - adecuada para crear capa `raw` + `curated`.

- **Proceso de corrección**
  - Puede implementarse como:
    - vistas SQL,
    - stored procedures,
    - o un ejecutable `.exe` que materialice tablas corregidas.

---

## Estructura de datos recomendada

### 1. Tabla cruda

Guardar exactamente lo que entrega el Shelly, sin modificar:

- timestamp recibido,
- timestamp enviado por Shelly,
- métricas por fase:
  - voltaje,
  - corriente,
  - potencia activa,
  - potencia aparente,
  - factor de potencia,
  - frecuencia,
- métricas totales,
- payload JSON original.

### 2. Tabla de ventanas de corrección

Registrar periodos inválidos o que requieren ajuste:

- fase afectada (`a`, `b`, `c`, `total`),
- inicio,
- fin,
- tipo de incidencia:
  - `missing_voltage`
  - `reversed_ct`
  - `manual_estimate`
- voltaje asumido cuando aplique,
- multiplicador cuando aplique,
- notas.

### 3. Capa curada

Puede ser:

- una **vista** (`readings_curated`), o
- una **tabla materializada** que el `.exe` regenere.

---

## Flujo técnico

1. El Shelly ejecuta un script JavaScript cada 60 segundos.
2. El script llama `EM.GetStatus`.
3. El script hace `HTTP.POST` al receptor local.
4. El receptor guarda el evento en PostgreSQL.
5. Las correcciones no alteran la tabla raw.
6. Un procedimiento SQL o un `.exe` genera la capa curada.

---

## Docker: stack recomendado

### Servicios

- `postgres`
- `receiver` (API local en Python o Node.js)
- opcional:
  - `adminer` o `pgadmin` para inspeccionar datos.

### Estructura sugerida del proyecto

```text
shelly-energy/
  docker-compose.yml
  .env
  receiver/
    Dockerfile
    app.py
    requirements.txt
  db/
    init/
      001_schema.sql
      002_functions.sql
      003_views.sql
  scripts/
    shelly_export.js
  tools/
    curator/
      curator.py
      requirements.txt
  docs/
    shelly_pipeline.md
```

---

## `docker-compose.yml` sugerido

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: shelly_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: shelly_energy
      POSTGRES_USER: shelly_user
      POSTGRES_PASSWORD: shelly_pass
    ports:
      - "5432:5432"
    volumes:
      - shelly_pg_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d

  receiver:
    build:
      context: ./receiver
    container_name: shelly_receiver
    restart: unless-stopped
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: shelly_energy
      DB_USER: shelly_user
      DB_PASSWORD: shelly_pass
      APP_PORT: 8765
    ports:
      - "8765:8765"
    depends_on:
      - postgres

  adminer:
    image: adminer
    container_name: shelly_adminer
    restart: unless-stopped
    ports:
      - "8080:8080"
    depends_on:
      - postgres

volumes:
  shelly_pg_data:
```

---

## Script JavaScript para el Shelly

Guardar como `scripts/shelly_export.js`.

> Cambiar la IP o hostname del receptor antes de usarlo.

```javascript
let SERVER_URL = "http://TU_IP_LOCAL:8765/shelly";
let EM_ID = 0;
let PERIOD_MS = 60000;
let sending = false;

function log(msg) {
  print("[energy-export] " + msg);
}

function postReading(payload) {
  Shelly.call(
    "HTTP.POST",
    {
      url: SERVER_URL,
      body: JSON.stringify(payload),
      content_type: "application/json",
      timeout: 10
    },
    function (res, err_code, err_msg) {
      if (err_code !== 0) {
        log("HTTP.POST error: " + err_code + " / " + err_msg);
      } else {
        log("POST ok");
      }
      sending = false;
    }
  );
}

function collectAndSend() {
  if (sending) {
    log("skip: previous send still running");
    return;
  }

  sending = true;

  Shelly.call("EM.GetStatus", { id: EM_ID }, function (res, err_code, err_msg) {
    if (err_code !== 0 || !res) {
      log("EM.GetStatus error: " + err_code + " / " + err_msg);
      sending = false;
      return;
    }

    let payload = {
      source: "shelly_pro_3em",
      em_id: EM_ID,
      sent_at_unix: Math.floor(Date.now() / 1000),
      reading: res
    };

    postReading(payload);
  });
}

Timer.set(5000, false, collectAndSend);
Timer.set(PERIOD_MS, true, collectAndSend);

log("script started");
```

---

## Servicio receptor recomendado

### Opción recomendada
Crear el receptor en **Python + FastAPI** o **Flask**.

### Responsabilidades del receptor

- exponer `POST /shelly`,
- validar payload,
- insertar en `readings_raw`,
- responder `200 OK`,
- registrar errores de parseo o inserción.

---

## SQL inicial sugerido

Guardar como `db/init/001_schema.sql`.

```sql
CREATE TABLE IF NOT EXISTS readings_raw (
    id BIGSERIAL PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source TEXT,
    em_id INTEGER,
    sent_at_unix BIGINT,

    a_voltage DOUBLE PRECISION,
    a_current DOUBLE PRECISION,
    a_act_power DOUBLE PRECISION,
    a_aprt_power DOUBLE PRECISION,
    a_pf DOUBLE PRECISION,
    a_freq DOUBLE PRECISION,

    b_voltage DOUBLE PRECISION,
    b_current DOUBLE PRECISION,
    b_act_power DOUBLE PRECISION,
    b_aprt_power DOUBLE PRECISION,
    b_pf DOUBLE PRECISION,
    b_freq DOUBLE PRECISION,

    c_voltage DOUBLE PRECISION,
    c_current DOUBLE PRECISION,
    c_act_power DOUBLE PRECISION,
    c_aprt_power DOUBLE PRECISION,
    c_pf DOUBLE PRECISION,
    c_freq DOUBLE PRECISION,

    n_current DOUBLE PRECISION,
    total_current DOUBLE PRECISION,
    total_act_power DOUBLE PRECISION,
    total_aprt_power DOUBLE PRECISION,

    raw_json JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS correction_windows (
    id BIGSERIAL PRIMARY KEY,
    phase TEXT NOT NULL CHECK (phase IN ('a', 'b', 'c', 'total')),
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL,
    issue_type TEXT NOT NULL CHECK (issue_type IN ('missing_voltage', 'reversed_ct', 'manual_estimate')),
    note TEXT,
    assumed_voltage DOUBLE PRECISION,
    multiplier DOUBLE PRECISION DEFAULT 1.0
);
```

---

## Stored procedures / funciones para corrección

Guardar como `db/init/002_functions.sql`.

```sql
CREATE OR REPLACE FUNCTION apply_missing_voltage_fix(
    p_current DOUBLE PRECISION,
    p_pf DOUBLE PRECISION,
    p_assumed_voltage DOUBLE PRECISION
)
RETURNS DOUBLE PRECISION
LANGUAGE SQL
AS $$
    SELECT COALESCE(p_current, 0) * COALESCE(p_pf, 1) * COALESCE(p_assumed_voltage, 127.0);
$$;

CREATE OR REPLACE FUNCTION apply_multiplier_fix(
    p_value DOUBLE PRECISION,
    p_multiplier DOUBLE PRECISION
)
RETURNS DOUBLE PRECISION
LANGUAGE SQL
AS $$
    SELECT COALESCE(p_value, 0) * COALESCE(p_multiplier, 1.0);
$$;
```

---

## Vista curada sugerida

Guardar como `db/init/003_views.sql`.

```sql
CREATE OR REPLACE VIEW readings_curated AS
SELECT
    r.*,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'a'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.a_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'a'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.a_act_power
    END AS a_act_power_fixed,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'b'
              AND cw.issue_type = 'missing_voltage'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_missing_voltage_fix(
            r.b_current,
            r.b_pf,
            (SELECT cw.assumed_voltage
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type = 'missing_voltage'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'b'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.b_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'b'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.b_act_power
    END AS b_act_power_fixed,

    CASE
        WHEN EXISTS (
            SELECT 1
            FROM correction_windows cw
            WHERE cw.phase = 'c'
              AND cw.issue_type = 'reversed_ct'
              AND r.received_at BETWEEN cw.start_at AND cw.end_at
        )
        THEN apply_multiplier_fix(
            r.c_act_power,
            (SELECT cw.multiplier
             FROM correction_windows cw
             WHERE cw.phase = 'c'
               AND cw.issue_type = 'reversed_ct'
               AND r.received_at BETWEEN cw.start_at AND cw.end_at
             ORDER BY cw.id DESC
             LIMIT 1)
        )
        ELSE r.c_act_power
    END AS c_act_power_fixed
FROM readings_raw r;
```

---

## Cómo registrar las correcciones de tu caso

### 1. Fase B sin referencia de voltaje

Se debe registrar una ventana `missing_voltage` para fase `b`.

Ejemplo:

```sql
INSERT INTO correction_windows
(phase, start_at, end_at, issue_type, note, assumed_voltage, multiplier)
VALUES
(
  'b',
  '2026-03-01 00:00:00+00',
  '2026-03-15 23:59:59+00',
  'missing_voltage',
  'Fase B sin voltaje de referencia; estimación por corriente x PF x voltaje asumido',
  127.0,
  1.0
);
```

### 2. CT invertido en una fase

Registrar la fase correspondiente como `reversed_ct` con `multiplier = -1.0`.

Ejemplo:

```sql
INSERT INTO correction_windows
(phase, start_at, end_at, issue_type, note, assumed_voltage, multiplier)
VALUES
(
  'c',
  '2026-03-01 00:00:00+00',
  '2026-03-10 12:00:00+00',
  'reversed_ct',
  'CT invertido; inversión de signo de la potencia activa',
  NULL,
  -1.0
);
```

---

## EXE para regenerar la capa curada

### Objetivo del ejecutable

Generar un `.exe` que:

1. se conecte a PostgreSQL,
2. lea `readings_raw`,
3. aplique o recalcule correcciones,
4. regenere una tabla `readings_curated_materialized`,
5. opcionalmente exporte CSV corregido.

### Recomendación técnica

Implementarlo en **Python** y compilar con **PyInstaller**.

### Flujo del ejecutable

- cargar configuración desde `.env`,
- ejecutar SQL:
  - truncar tabla materializada,
  - volver a insertar datos corregidos,
- opcional:
  - exportar a CSV,
  - generar bitácora de ejecución.

### Comando sugerido para compilar

```bash
pyinstaller --onefile --name shelly_curator curator.py
```

---

## Lógica sugerida del `curator.py`

- conectar a PostgreSQL,
- crear si no existe `readings_curated_materialized`,
- poblarla desde `readings_curated`,
- recalcular columnas totales corregidas:
  - `total_act_power_fixed = a_act_power_fixed + b_act_power_fixed + c_act_power_fixed`,
- exportar a CSV opcional.

---

## Prompt para el agente de Antigravity

Copiar y pegar tal cual:

```text
Quiero que implementes una solución técnica completa para un Shelly Pro 3EM con persistencia local y corrección de datos históricos.

Contexto:
- Ya tengo Docker instalado.
- Quiero usar una base de datos dentro de Docker, preferentemente PostgreSQL.
- El Shelly Pro 3EM debe ejecutar un script JavaScript interno para extraer la telemetría usando RPC EM.GetStatus y enviarla por HTTP POST a un receptor local.
- El receptor debe correr también en Docker y guardar todo en una tabla raw sin alterar el payload original.
- Necesito una segunda capa curada para corregir datos históricos contaminados.

Incidencias a corregir:
1. Durante aproximadamente 15 días, la fase B no tenía conectada la referencia de voltaje, por lo que no registró los ~125 V correctamente.
2. Durante un periodo adicional, uno de los CT estuvo invertido y la energía/potencia se registró como retorno en lugar de consumo.
3. Quiero conservar la tabla raw original y aplicar las correcciones sobre una vista o tabla materializada curada.

Requerimientos:
1. Genera la estructura completa del proyecto:
   - docker-compose.yml
   - servicio postgres
   - servicio receptor HTTP
   - scripts SQL de inicialización
   - script JavaScript del Shelly
   - herramienta Python para materializar y corregir datos
2. Usa PostgreSQL.
3. Crea estas tablas como mínimo:
   - readings_raw
   - correction_windows
4. Crea funciones SQL y vistas o procedimientos para:
   - estimar potencia cuando falta voltaje de referencia usando corriente x PF x voltaje asumido
   - invertir signo cuando el CT estuvo al revés
5. Genera una tabla o vista `readings_curated`.
6. Genera un programa Python `curator.py` que:
   - se conecte a PostgreSQL
   - recalcule una tabla materializada curada
   - exporte CSV opcional
7. Genera también el paso para compilar ese script como `.exe` usando PyInstaller.
8. El receptor HTTP debe aceptar `POST /shelly` y guardar JSON y columnas normalizadas.
9. El proyecto debe quedar listo para levantar con `docker compose up -d`.
10. Incluye README.md con:
   - prerequisitos
   - configuración de variables
   - cómo obtener IP local
   - cómo configurar el script en Shelly
   - cómo validar que el receptor recibe datos
   - cómo insertar ventanas de corrección
   - cómo regenerar la capa curada
   - cómo compilar y usar el `.exe`

Entregables:
- código fuente completo
- archivos SQL
- script Shelly JavaScript
- receptor HTTP
- script curator.py
- instrucciones claras para ejecutar todo de extremo a extremo
- decisiones técnicas documentadas

Consideraciones:
- Mantener la tabla raw inmutable.
- Hacer las correcciones sin sobrescribir los datos originales.
- Diseñar para uso local en red doméstica.
- Priorizar simplicidad de operación y trazabilidad de las correcciones.
```

---

## Pasos operativos recomendados

### Fase 1
Levantar Docker:

```bash
docker compose up -d
```

### Fase 2
Confirmar base de datos y receptor:
- PostgreSQL en `localhost:5432`
- receptor en `localhost:8765`
- Adminer en `localhost:8080`

### Fase 3
Cargar script al Shelly:
- abrir Web UI,
- ir a Scripts,
- crear script nuevo,
- pegar `shelly_export.js`,
- ajustar IP del receptor,
- ejecutar y habilitar.

### Fase 4
Validar datos crudos:
- revisar `readings_raw`,
- verificar timestamps y campos por fase.

### Fase 5
Registrar ventanas de corrección:
- insertar `missing_voltage` para fase B,
- insertar `reversed_ct` para la fase afectada.

### Fase 6
Ejecutar curación:
- correr `curator.py`,
- compilar `.exe` si se requiere,
- regenerar capa curada.

---

## Cómo funcionan los scripts del Shelly

Los scripts en Shelly son JavaScript reducido que corre dentro del equipo y puede:

- ejecutar timers,
- llamar métodos RPC locales mediante `Shelly.call(...)`,
- hacer llamadas HTTP,
- reaccionar a eventos,
- registrar logs.

En este caso se usan como un **agente extractor**.

No son una base de datos ni deben usarse para corrección retrospectiva del histórico.
Su función aquí es:

1. leer telemetría,
2. enviarla a infraestructura local,
3. dejar la corrección para la base de datos y el proceso de curación.

---

## Recomendación final

Para tu caso conviene:

- **PostgreSQL en Docker**
- **receptor HTTP en Docker**
- **tabla raw inmutable**
- **ventanas de corrección documentadas**
- **vista o tabla curada**
- **`.exe` para regenerar la capa curada cuando lo necesites**

Eso te deja una solución ordenada, trazable y fácil de auditar.
