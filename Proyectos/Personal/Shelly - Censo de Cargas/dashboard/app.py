import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Shelly Pro 3EM Analytics", layout="wide", page_icon="⚡")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shelly_energy")
DB_USER = os.getenv("DB_USER", "shelly_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "shelly_pass")

@st.cache_resource
def get_db_connection():
    try:
        return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except Exception as e:
        st.error(f"Error connecting to DB: {e}")
        return None

def fetch_data(query, params=None):
    conn = get_db_connection()
    if conn:
        return pd.read_sql(query, conn, params=params)
    return pd.DataFrame()

# UI Layout Navigation
st.sidebar.title("Navegación / Navigation")
page = st.sidebar.radio("Ir a", ["Visión General (Generics)", "Detalle por Fase (Phase Details)", "Análisis de Picos (Peak Detection)", "Calidad de Datos", "Mantenimiento / Salud"])

# Common Filters
st.sidebar.header("Filtros Globales")
time_range = st.sidebar.selectbox("Rango de Tiempo", ["Últimas 24 horas", "Últimos 7 días", "Últimos 30 días", "Personalizado"])

start_date = None
end_date = None
if time_range == "Personalizado":
    start_date = st.sidebar.date_input("Fecha Inicio", value=datetime.today() - timedelta(days=1))
    end_date = st.sidebar.date_input("Fecha Fin", value=datetime.today())
else:
    now = datetime.utcnow()
    if time_range == "Últimas 24 horas":
         start_date = now - timedelta(days=1)
    elif time_range == "Últimos 7 días":
         start_date = now - timedelta(days=7)
    elif time_range == "Últimos 30 días":
         start_date = now - timedelta(days=30)
         
def get_core_dataframe():
    query = f"""
        SELECT received_at, 
               COALESCE(a_act_power_fixed, 0) as a_act_power, COALESCE(a_aprt_power, 0) as a_aprt_power,
               COALESCE(b_act_power_fixed, 0) as b_act_power, COALESCE(b_aprt_power, 0) as b_aprt_power,
               COALESCE(c_act_power_fixed, 0) as c_act_power, COALESCE(c_aprt_power, 0) as c_aprt_power,
               COALESCE(a_act_power_fixed, 0) + COALESCE(b_act_power_fixed, 0) + COALESCE(c_act_power_fixed, 0) as total_act_power,
               COALESCE(total_aprt_power, 0) as total_aprt_power,
               COALESCE(a_current, 0) as a_current, COALESCE(b_current, 0) as b_current, COALESCE(c_current, 0) as c_current,
               COALESCE(a_voltage, 0) as a_voltage, COALESCE(b_voltage, 0) as b_voltage, COALESCE(c_voltage, 0) as c_voltage,
               a_pf, b_pf, c_pf,
               COALESCE(a_energy, 0) as a_energy, COALESCE(b_energy, 0) as b_energy, COALESCE(c_energy, 0) as c_energy, COALESCE(total_energy, 0) as total_energy
        FROM readings_curated
        WHERE received_at >= %s
        ORDER BY received_at ASC
    """
    return fetch_data(query, (start_date,))

if page == "Visión General (Generics)":
    st.title("⚡ Visión General de Energía")
    df = get_core_dataframe()
    
    if not df.empty:
        # Metricas Principales
        st.subheader("Indicadores de Totales (Consolidado)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Potencia Total (W)", f"{df['total_act_power'].iloc[-1]:.1f} W")
        c2.metric("Potencia Aparente (VA)", f"{df['total_aprt_power'].iloc[-1]:.1f} VA")
        c3.metric("Pico Máximo", f"{df['total_act_power'].max():.1f} W")
        
        # Determine Energy. Since the counter is cumulative, subtracting last from first gives delta in period
        if df['total_energy'].iloc[-1] > df['total_energy'].iloc[0]:
            energy_consumed = df['total_energy'].iloc[-1] - df['total_energy'].iloc[0]
            c4.metric("Energía Consumida (Periodo)", f"{energy_consumed:.1f} Wh")
        else:
             c4.metric("Promedio de Consumo", f"{df['total_act_power'].mean():.1f} W") 

        st.markdown("---")
        
        # Grafica Combinada
        st.subheader("Tendencia de Consumo Activo (A, B, C vs Total)")
        plot_df = pd.melt(df, id_vars=['received_at'], value_vars=['a_act_power', 'b_act_power', 'c_act_power', 'total_act_power'])
        
        fig = px.line(plot_df, x="received_at", y="value", color="variable",
                      labels={"value": "Potencia Activa (W)", "received_at": "Tiempo", "variable": "Fase"},
                      color_discrete_map={
                          "a_act_power": "#1f77b4",
                          "b_act_power": "#ff7f0e",
                          "c_act_power": "#2ca02c",
                          "total_act_power": "red"
                      })
        fig.update_traces(line=dict(width=1.5))
        for trace in fig.data:
            if trace.name == "total_act_power":
                trace.line.width = 4
        st.plotly_chart(fig, use_container_width=True)

elif page == "Detalle por Fase (Phase Details)":
    st.title("📊 Análisis Profundo por Fase")
    phases = st.multiselect("Fases a visualizar / comparar", ["Fase A", "Fase B", "Fase C"], default=["Fase A", "Fase B", "Fase C"])
    df = get_core_dataframe()

    if not df.empty:
        # Create Phase Cards
        cols = st.columns(3)
        
        phase_map = {
            "Fase A": ("a_act_power", "a_aprt_power", "a_current", "a_voltage", "a_pf", "a_energy", cols[0]),
            "Fase B": ("b_act_power", "b_aprt_power", "b_current", "b_voltage", "b_pf", "b_energy", cols[1]),
            "Fase C": ("c_act_power", "c_aprt_power", "c_current", "c_voltage", "c_pf", "c_energy", cols[2])
        }
        
        for phase_name in phases:
            act, aprt, cur, volt, pf, engy, col = phase_map[phase_name]
            with col:
                st.subheader(phase_name)
                st.metric("Power (W)", f"{df[act].iloc[-1]:.1f}", f"Avg: {df[act].mean():.1f}")
                st.metric("Apparent (VA)", f"{df[aprt].iloc[-1]:.1f}")
                st.metric("Current (A)", f"{df[cur].iloc[-1]:.2f}")
                
                # Replace explicitly missing/0 voltage stats thoughtfully 
                valid_v = df[df[volt] > 0][volt]
                v_avg = valid_v.mean() if not valid_v.empty else 0
                st.metric("Voltage (V)", f"{df[volt].iloc[-1]:.1f}", f"Avg: {v_avg:.1f}")
                
                st.metric("Power Factor (PF)", f"{df[pf].iloc[-1]:.2f}")
                
                energy_diff = df[engy].iloc[-1] - df[engy].iloc[0] if df[engy].iloc[-1] >= df[engy].iloc[0] else 0
                st.metric("Energy (Wh)", f"{energy_diff:.1f}")

        st.markdown("---")
        
        st.subheader("Comparativa de Voltaje y Corriente")
        v_cols = [phase_map[p][3] for p in phases]
        c_cols = [phase_map[p][2] for p in phases]
        
        tab1, tab2, tab3 = st.tabs(["Voltaje (V)", "Corriente (A)", "Factor de Potencia (PF)"])
        with tab1:
            fig_v = px.line(pd.melt(df, id_vars=['received_at'], value_vars=v_cols), x="received_at", y="value", color="variable", title="Estabilidad de Voltaje")
            st.plotly_chart(fig_v, use_container_width=True)
        with tab2:
            fig_c = px.line(pd.melt(df, id_vars=['received_at'], value_vars=c_cols), x="received_at", y="value", color="variable", title="Corriente Demandada")
            st.plotly_chart(fig_c, use_container_width=True)
        with tab3:
            pf_cols = [phase_map[p][4] for p in phases]
            fig_pf = px.line(pd.melt(df, id_vars=['received_at'], value_vars=pf_cols), x="received_at", y="value", color="variable", title="Factor de Potencia")
            st.plotly_chart(fig_pf, use_container_width=True)

elif page == "Análisis de Picos (Peak Detection)":
    st.title("🚨 Detección de Picos y Anomalías")
    df = get_core_dataframe()
    
    if not df.empty:
        n_peaks = st.slider("Cantidad de picos a mostrar", 5, 50, 10)
        
        st.subheader(f"Top {n_peaks} picos de Consumo Total Registrados")
        top_total = df[['received_at', 'total_act_power', 'a_act_power', 'b_act_power', 'c_act_power']].sort_values(by='total_act_power', ascending=False).head(n_peaks)
        st.dataframe(top_total, use_container_width=True)

        st.subheader(f"Top {n_peaks} picos por Fase Individual")
        col1, col2, col3 = st.columns(3)
        with col1:
             st.write("🔌 Fase A")
             st.dataframe(df[['received_at', 'a_act_power']].sort_values(by='a_act_power', ascending=False).head(n_peaks))
        with col2:
             st.write("🔌 Fase B")
             st.dataframe(df[['received_at', 'b_act_power']].sort_values(by='b_act_power', ascending=False).head(n_peaks))
        with col3:
             st.write("🔌 Fase C")
             st.dataframe(df[['received_at', 'c_act_power']].sort_values(by='c_act_power', ascending=False).head(n_peaks))
             
        # Gráfica destacando los picos contra el promedio
        avg = df['total_act_power'].mean()
        fig = px.scatter(df, x="received_at", y="total_act_power", title="Dispersión del Consumo Total vs Promedio")
        fig.add_hline(y=avg, line_dash="solid", annotation_text="Promedio", annotation_position="bottom right", line_color="green")
        
        p95 = df['total_act_power'].quantile(0.95)
        fig.add_hline(y=p95, line_dash="dot", annotation_text="Percentil 95 (Picos)", annotation_position="top right", line_color="red")
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "Calidad de Datos":
    st.title("🛡️ Calidad de Datos e Imputaciones")
    st.write("Ventanas de corrección activas ingresadas en la Base de Datos para limpiar los datos crudos.")
    windows_df = fetch_data("SELECT * FROM correction_windows ORDER BY start_at DESC")
    st.dataframe(windows_df, use_container_width=True)

elif page == "Mantenimiento / Salud":
    st.title("🏥 Salud y Base de Datos Crudos")
    st.write(f"Conexión a PostgreSQL: {'🟢 ONLINE' if get_db_connection() else '🔴 OFFLINE'}")
    
    last_record_query = "SELECT received_at, total_act_power, total_energy FROM readings_raw ORDER BY received_at DESC LIMIT 1"
    last_record = fetch_data(last_record_query)
    
    if not last_record.empty:
        last_time = last_record.iloc[0]['received_at']
        st.write(f"Último latido recibido: **{last_time}**")
        
        diff = (datetime.now(last_time.tzinfo) - last_time).total_seconds()
        if diff < 120:
             st.success(f"La base de datos recibe el heartbeat de Shelly de forma saludable (hace {diff:.1f} segundos).")
        else:
             st.error(f"⚠️ El pipeline está detenido. Hace {diff/60:.1f} minutos que Shelly no reporta o el importador no ha finalizado.")
             
    st.markdown("### Explorador de Base de Datos Base Cruda")
    raw_df = fetch_data("SELECT received_at, a_act_power, b_act_power, c_act_power, total_energy, a_voltage, b_voltage, c_voltage FROM readings_raw ORDER BY received_at DESC LIMIT 500")
    st.dataframe(raw_df)
    
    if not raw_df.empty:
        csv = raw_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Descargar Últimos 500 Registros (CSV)", data=csv, file_name="shelly_datos_crudos_recientes.csv", mime="text/csv")
