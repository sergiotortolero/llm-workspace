import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
import psycopg2

app = FastAPI(title="Shelly Receiver")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "shelly_energy"),
            user=os.getenv("DB_USER", "shelly_user"),
            password=os.getenv("DB_PASSWORD", "shelly_pass")
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/health")
def health_check():
    return {"ok": True, "ts": datetime.utcnow().isoformat() + "Z"}

@app.post("/shelly")
async def receive_shelly_data(request: Request):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    reading = payload.get("reading", {})
    source = payload.get("source", "shelly_pro_3em")
    em_id = payload.get("em_id", 0)
    sent_at_unix = payload.get("sent_at_unix", int(datetime.utcnow().timestamp()))

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO readings_raw (
                    source, em_id, sent_at_unix,
                    a_voltage, a_current, a_act_power, a_aprt_power, a_pf, a_freq, a_energy,
                    b_voltage, b_current, b_act_power, b_aprt_power, b_pf, b_freq, b_energy,
                    c_voltage, c_current, c_act_power, c_aprt_power, c_pf, c_freq, c_energy,
                    n_current, total_current, total_act_power, total_aprt_power, total_energy,
                    raw_json
                ) VALUES (
                    %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s
                )
            """, (
                source, em_id, sent_at_unix,

                reading.get("a_voltage"), reading.get("a_current"), reading.get("a_act_power"),
                reading.get("a_aprt_power"), reading.get("a_pf"), reading.get("a_freq"), reading.get("a_total"),

                reading.get("b_voltage"), reading.get("b_current"), reading.get("b_act_power"),
                reading.get("b_aprt_power"), reading.get("b_pf"), reading.get("b_freq"), reading.get("b_total"),

                reading.get("c_voltage"), reading.get("c_current"), reading.get("c_act_power"),
                reading.get("c_aprt_power"), reading.get("c_pf"), reading.get("c_freq"), reading.get("c_total"),

                reading.get("n_current"), reading.get("total_current"), reading.get("total_act_power"),
                reading.get("total_aprt_power"), reading.get("total"),

                json.dumps(payload, ensure_ascii=False)
            ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database insert error: {e}")
    finally:
        conn.close()

    return {"ok": True}
