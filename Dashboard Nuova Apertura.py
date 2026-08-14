import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard CDA", layout="wide")
st.title("📊 Dashboard Analitica CDA 2026")

# Carica i dati direttamente dall'Excel presente nella repository
try:
    df = pd.read_excel('APRI_DASHBOARD_2026 (1).xlsx', sheet_name='APRI')
    st.sidebar.success("Dati caricati correttamente!")
except:
    st.sidebar.error("File Excel non trovato. Assicurati che il nome sia identico.")

# Sidebar: Input (Logica semplificata basata sulle tue colonne)
st.sidebar.header("Parametri")
incassi_base = st.sidebar.slider("Incassi A1", 4000, 10000, 4800)

# Visualizzazione completa del Conto Economico
st.subheader("Conto Economico di Progetto")
st.dataframe(df, use_container_width=True) # Qui vedrai tutto l'Excel

# Analisi Finanziaria
st.subheader("Analisi CFO (Struttura Finanziaria)")
# Supponiamo che il tuo Excel abbia colonne 'Cassa' e 'Banca'
if 'Saldo Banca' in df.columns:
    st.line_chart(df['Saldo Banca'])
else:
    st.info("Colonna 'Saldo Banca' non trovata nel file Excel.")
