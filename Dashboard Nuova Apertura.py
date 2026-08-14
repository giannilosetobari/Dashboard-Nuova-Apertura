import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Dashboard CDA 2026", layout="wide")

# --- TITOLO E HEADER ---
st.title("📊 Progetto Apertura 2026 | Analisi Strategica CDA")
st.markdown("---")

# --- SIDEBAR: INPUT DINAMICI (IL MOTORE) ---
st.sidebar.header("⚙️ Parametri Strategici")
incassi_base = st.sidebar.slider("Volume Incassi Anno 1 (€)", 4000, 7000, 4800)
costo_lavoro_perc = st.sidebar.slider("Incidenza Costo Lavoro (%)", 0.05, 0.20, 0.118, format="%.3f")
margine_lordo_perc = st.sidebar.slider("Margine Lordo (%)", 0.10, 0.30, 0.19, format="%.2f")

# --- LOGICA DI CALCOLO (MOTORE) ---
def calcola_modello(incassi_a1, c_lav, marg):
    incassi = [incassi_a1, incassi_a1 * 1.104, incassi_a1 * 1.208, incassi_a1 * 1.243]
    margine = [i * marg for i in incassi]
    lavoro = [i * c_lav for i in incassi]
    fissi = [400, 410, 420, 430] # Spese generali simulate
    
    utile = [(margine[i] - lavoro[i] - fissi[i]) for i in range(4)]
    saldo_banca = [-158 + (u * 0.5) for u in utile] # Simulazione impatto tesoreria
    
    return pd.DataFrame({
        "Anno": [1, 2, 3, 4],
        "Incassi": incassi,
        "Margine Operativo": utile,
        "Saldo Banca (CFO)": saldo_banca
    })

df = calcola_modello(incassi_base, costo_lavoro_perc, margine_lordo_perc)

# --- TAB: LAYOUT CDA ---
tab1, tab2 = st.tabs(["📈 Visione Strategica (Conto Economico)", "🏦 Analisi di Tesoreria (CFO)"])

with tab1:
    st.subheader("Conto Economico Previsionale")
    st.dataframe(df[["Anno", "Incassi", "Margine Operativo"]].style.format("{:.2f}"), use_container_width=True)
    st.line_chart(df.set_index("Anno")[["Incassi", "Margine Operativo"]])

with tab2:
    st.subheader("Analisi di Sostenibilità Finanziaria")
    st.markdown("Monitoraggio dell'esposizione bancaria e flussi di cassa.")
    
    # Alert logico per il CFO
    if df["Saldo Banca (CFO)"].min() < -180:
        st.error("⚠️ ALERT CFO: L'esposizione bancaria supera la soglia di rischio in uno degli anni simulati.")
    else:
        st.success("✅ Valutazione CFO: La struttura finanziaria rientra nei parametri di tolleranza.")
        
    st.bar_chart(df.set_index("Anno")["Saldo Banca (CFO)"])
    st.table(df[["Anno", "Saldo Banca (CFO)"]])

st.markdown("---")
st.caption("Strumento di supporto alla decisione CDA - Analisi Dinamica 2026")