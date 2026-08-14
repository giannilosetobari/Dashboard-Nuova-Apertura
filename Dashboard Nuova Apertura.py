import streamlit as st
import pandas as pd

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Dashboard CDA 2026", layout="wide")

# --- CARICAMENTO DATI ---
@st.cache_data
def load_data():
    # Assicurati che il file 'dati.xlsx' sia nella stessa cartella
    df_apri = pd.read_excel('dati.xlsx', sheet_name='APRI')
    df_calc = pd.read_excel('dati.xlsx', sheet_name='CALCOLI')
    return df_apri, df_calc

try:
    df_apri, df_calc = load_data()
except Exception as e:
    st.error(f"Errore nel caricamento file: {e}")
    st.stop()

# --- SIDEBAR: LEVE DI INPUT ---
st.sidebar.header("🎛️ Pannello di Controllo")
incassi_a1 = st.sidebar.slider("Volume Incassi Anno 1 (€)", 4000, 8000, 4800, 100)
margine = st.sidebar.slider("Margine Lordo (%)", 0.10, 0.30, 0.19, 0.01)

# --- MOTORE DI CALCOLO ---
anni = ["Anno 1", "Anno 2", "Anno 3", "Anno 4"]
fattori = [1.0, 1.104, 1.208, 1.243]
incassi = [incassi_a1 * f for f in fattori]
utile_op = [i * margine * 0.4 for i in incassi] # Esempio di calcolo derivato

df_sim = pd.DataFrame({
    "Periodo": anni,
    "Incassi": incassi,
    "Margine Lordo": [i * margine for i in incassi],
    "Utile Operativo": utile_op
})

# --- LAYOUT A TAB ---
tab1, tab2, tab3 = st.tabs(["📈 Visione CEO", "🏦 Controllo CFO", "📑 Dati Grezzi"])

with tab1:
    st.subheader("Sintesi Economica Strategica")
    st.metric("Fatturato Anno 4", f"€ {incassi[3]:,.2f}")
    st.line_chart(df_sim.set_index("Periodo")[["Incassi", "Utile Operativo"]])
    st.dataframe(df_sim)

with tab2:
    st.subheader("Analisi di Tesoreria")
    st.info("Monitoraggio flussi di cassa e posizioni bancarie.")
    st.bar_chart(df_sim.set_index("Periodo")["Utile Operativo"])

with tab3:
    st.subheader("Consultazione Excel")
    st.dataframe(df_apri)
