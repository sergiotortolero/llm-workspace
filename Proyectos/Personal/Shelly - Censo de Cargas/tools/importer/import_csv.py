import os
import sys
import pandas as pd
import psycopg2
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shelly_energy")
DB_USER = os.getenv("DB_USER", "shelly_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "shelly_pass")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def fix_column_names(df):
    # Shelly standard export normalizes generic names. Map them to our DB schema if needed
    col_map = {
        'Time': 'received_at',
        'Active energy A (Wh)': 'a_energy',
        'Active power A (W)': 'a_act_power',
        'Apparent power A (VA)': 'a_aprt_power',
        'Voltage A (V)': 'a_voltage',
        'Current A (A)': 'a_current',
        'Active energy B (Wh)': 'b_energy',
        'Active power B (W)': 'b_act_power',
        'Apparent power B (VA)': 'b_aprt_power',
        'Voltage B (V)': 'b_voltage',
        'Current B (A)': 'b_current',
        'Active energy C (Wh)': 'c_energy',
        'Active power C (W)': 'c_act_power',
        'Apparent power C (VA)': 'c_aprt_power',
        'Voltage C (V)': 'c_voltage',
        'Current C (A)': 'c_current',
        'Active energy Total (Wh)': 'total_energy',
        'Active power Total (W)': 'total_act_power',
        'Apparent power Total (VA)': 'total_aprt_power'
    }
    df.rename(columns=col_map, inplace=True)
    return df

def import_csv(file_path):
    print(f"Leyendo archivo CSV: {file_path}")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error cargando CSV: {e}")
        return

    df = fix_column_names(df)
    
    if 'received_at' not in df.columns:
        print("❌ El archivo CSV no tiene la columna 'Time' o no es un export válido de Shelly.")
        return

    print("Conectando a la base de datos...")
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Process rows
    inserted = 0
    skipped = 0
    
    for index, row in df.iterrows():
        dt = pd.to_datetime(row['received_at'])
        
        # Avoid duplicate timestamps
        cur.execute("SELECT 1 FROM readings_raw WHERE received_at = %s", (dt,))
        if cur.fetchone() is not None:
             skipped += 1
             continue

        cur.execute("""
            INSERT INTO readings_raw (
                received_at, source, em_id, sent_at_unix,
                a_voltage, a_current, a_act_power, a_aprt_power, a_energy,
                b_voltage, b_current, b_act_power, b_aprt_power, b_energy,
                c_voltage, c_current, c_act_power, c_aprt_power, c_energy,
                total_act_power, total_aprt_power, total_energy,
                raw_json
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s
            )
        """, (
            dt, "csv_import", 0, int(dt.timestamp()),
            
            row.get('a_voltage', 0), row.get('a_current', 0), row.get('a_act_power', 0), row.get('a_aprt_power', 0), row.get('a_energy', 0),
            row.get('b_voltage', 0), row.get('b_current', 0), row.get('b_act_power', 0), row.get('b_aprt_power', 0), row.get('b_energy', 0),
            row.get('c_voltage', 0), row.get('c_current', 0), row.get('c_act_power', 0), row.get('c_aprt_power', 0), row.get('c_energy', 0),
            
            row.get('total_act_power', 0), row.get('total_aprt_power', 0), row.get('total_energy', 0),
            '{"imported_from_csv": true}'
        ))
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✅ Proceso completo. Insertados: {inserted}. Omitidos (ya existían): {skipped}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python import_csv.py <ruta_al_archivo_csv>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    import_csv(file_path)
