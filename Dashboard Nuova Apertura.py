import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard CDA", layout="wide")
st.title("📊 Dashboard Analitica CDA 2026")

# Caricamento del file Excel senza vincoli rigidi sul nome del foglio
try:
    df = pd.read_excel('dati.xlsx', sheet_name=0)
    st.sidebar.success("File Excel caricato con successo!")
except Exception as e:
    st.sidebar.error(f"Errore: {e}")
    st.stop()

# Sidebar: Parametri
st.sidebar.header("Parametri")
incassi_base = st.sidebar.slider("Incassi A1", 4000, 10000, 4800)

# Visualizzazione Conto Economico
st.subheader("Conto Economico di Progetto")
st.dataframe(df, use_container_width=True)

# Sezione Finanziaria di Controllo (CFO)
st.subheader("Analisi di Tesoreria (CFO)")
if 'Saldo Banca' in df.columns:
    st.line_chart(df['Saldo Banca'])
else:
    st.info("Dati tabellari caricati correttamente.")
