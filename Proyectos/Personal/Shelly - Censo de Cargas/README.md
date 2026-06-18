# Shelly Pro 3EM - Postgres Telemetry Pipeline

Solución local para persistir y curar datos exportados mediante el medidor Shelly Pro 3EM.

## Requisitos
- Docker y Docker Compose
- Shelly Pro 3EM conectado a la misma red de área local

## 1. Configuración de Variables
Edita el archivo `.env` en el directorio raíz para modificar credenciales del servidor si es necesario. Por omisión se usarán credenciales predeterminadas sugeridas para un ámbito local (`shelly_energy`, `shelly_user`, `shelly_pass`).

## 2. Iniciar Servicios
Para levantar la base de datos PostgreSQL, la API Receptora en Python y el entorno Adminer:

```bash
docker compose up -d
```

Verifica la API Receptora (en el mismo PC que aloja Docker):
- Health check: `http://localhost:8765/health`

## 3. Configurar Script del Shelly
1. Abre la interfaz web de tu Shelly Pro 3EM (escribiendo su IP en el navegador).
2. Ve al menú `Scripts` y presiona `+ Create new script`.
3. Pega el contenido íntegro del archivo `scripts/shelly_export.js`.
4. **IMPORTANTE:** Cambia en el script la variable `SERVER_URL` por la IP local del computador donde corre el servicio Docker (ej. `http://192.168.1.15:8765/shelly`).
5. `Save` (Guardar) y luego comienza la ejecución dándole a `Start`. 
6. Habilita el interruptor `Enable` para que se ejecute de nuevo si el Shelly se reinicia.

## 4. Validar Recepción y Vista de Datos
Ingresa a **Adminer** navegando en el equipo Docker a `http://localhost:8080`.
- **System**: PostgreSQL
- **Server**: postgres (o localhost si lo corres desde fuera)
- **Username**: shelly_user 
- **Password**: shelly_pass
- **Database**: shelly_energy

Podrás ver cómo inicia el llenado de la tabla `readings_raw`.

## 5. Inserción de Correcciones
Los datos crudos NUNCA se editan. Si observaste errores (CT invertido, voltaje desconectado temporalmente, etc), agrega una regla a la tabla `correction_windows`.

Ejemplo para Fase B sin voltaje de referencia en marzo 2026, usando imputación base de 4.8 W (basado en estadísticas de capturas: 114.6 Wh promedio/hora = 4.8W):
```sql
INSERT INTO correction_windows
(phase, start_at, end_at, issue_type, note, assumed_voltage, assumed_power, multiplier)
VALUES
(
  'b',
  '2026-03-01 00:00:00+00',
  '2026-03-15 23:59:59+00',
  'manual_estimate',
  'Fase B sin voltaje; estimación plana de potencia usando media horaria de 4.8W (4.8Wh media vs 1h)',
  126.1,
  4.8,
  1.0
);
```

Ejemplo para CT invertido en fase C:
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

Una vez ingresadas las reglas, la Base de Datos automáticamente construirá y aplicará la lógica en la vista `readings_curated`.

## 6. Curación en Lote (Curator Tool) y Compilación del `.exe`
Puedes materializar estas correcciones y regenerar en formato CSV o en una tabla materializada (`readings_curated_materialized`) corriendo el script `curator.py`.

Para ejecutar este script en Python:
```bash
cd tools/curator
pip install -r requirements.txt
python curator.py
```

### 7. Ejecutable `shelly_launcher.exe`
Se ha generado un archivo `.exe` compilado nativamente para lanzar todo sin necesidad de comandos.
Lo encontrarás en: `dist/shelly_launcher.exe`.

Al ejecutarlo:
1. Verificará que Docker Desktop esté abierto.
2. Levantará `docker-compose up -d`.
3. Esperará unos segundos a que levanten Postgres, el backend y Streamlit.
4. Abrirá automáticamente el dashboard interactivo en tu navegador por defecto (`http://localhost:8501`).

### 8. Dashboard de Streamlit
El aplicativo incluye una pantalla interactiva con:
- **Visión General**: Gráficas consolidadas del consumo A, B, C vs Total y tarjetas con indicadores sumariados.
- **Análisis por Fase**: Gráficas independientes de estabilidad de Voltaje, Corriente, Energía consumida y Factor de Potencia por cada línea.
- **Detección de Picos**: Análisis percentil del top N picos generales y picos puntuales en Fases individuales.
- **Calidad de Datos**: Muestra el histórico de filtros y ventanas de corrección ingresadas en base de datos.
- **Salud del Sistema**: Valida que los datos estén ingresando sincronizadamente en el último minuto y otorga una exportación de la base cruda.

### 9. Importar Histórico de Datos Pasados (Shelly Export)
El Shelly Pro 3EM guarda localmente en su memoria interna 60 días de histórico, sin embargo, la API técnica de control no permite extracciones en lote retroactivas profundas sin integrarse a la nube autenticada. Para el modelo 100% local, el sistema incluye un extractor que ingesta el CSV original oficial del dispositivo.
1. Entra con tu navegador a la IP de tu Shelly.
2. Descarga el histórico local seleccionando el formato **CSV** por fase/total.
3. Guarda el archivo `.csv` descargado.
4. Para evitar sobre-escribir y cargar, abre tu terminal desde la raíz de este proyecto y ejecuta: `python tools/importer/import_csv.py "tu_archivo_descargado.csv"`
El script parseará y acomodará los nombres de columna del Excel de Shelly, insertándolos y rellenando los vacíos minuto a minuto dentro de la base de datos de PostgreSQL `readings_raw` para unificarlos al pipeline en tiempo real.

---

> **Nota Técnica:** Se ha incorporado en los scripts `.sql` de DB un sistema para imputar un consumo fijo y compensar un subregistro de potencia mediante los campos de `assumed_power` y estrategias combinadas, respaldado visualmente en **Streamlit**. El archivo `scripts/shelly_export.js` ya incluye tu IP local evaluada (`192.168.3.95`) para enviar datos con **Energía Total (Wh)** integrada cada 60 segundos.
