import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

# Load environment variables (useful if running outside docker, .env at project root)
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shelly_energy")
DB_USER = os.getenv("DB_USER", "shelly_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "shelly_pass")

def get_db_connection():
    print(f"Connecting to Postgres at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def materialize_and_export():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Step 1: Create or replace materialized table logic
        print("Regenerating readings_curated_materialized...")
        
        cur.execute("DROP TABLE IF EXISTS readings_curated_materialized;")
        cur.execute("""
            CREATE TABLE readings_curated_materialized AS
            SELECT *,
                   (COALESCE(a_act_power_fixed, 0) + 
                    COALESCE(b_act_power_fixed, 0) + 
                    COALESCE(c_act_power_fixed, 0)) AS total_act_power_fixed
            FROM readings_curated;
        """)
        conn.commit()

        # Step 2: Export to CSV (optional)
        print("Exporting data to CSV...")
        query = "SELECT * FROM readings_curated_materialized ORDER BY received_at DESC"
        df = pd.read_sql_query(query, conn)
        
        csv_filename = "shelly_energy_curated.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data successfully exported to {csv_filename} ({len(df)} rows).")

    except Exception as e:
        print(f"Error during curation: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    print("Starting curation process...")
    materialize_and_export()
    print("Process complete.")
