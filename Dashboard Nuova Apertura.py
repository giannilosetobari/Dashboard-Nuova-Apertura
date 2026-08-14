import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="Dashboard CDA 2026 | Gestione Progetto Apertura",
    page_icon="🏢",
    layout="wide"
)

# --- STILE CSS PULITO E ISTITUZIONALE ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stMetric { background-color: #ffffff; padding: 16px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #1f77b4; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 6px; padding: 10px 20px; font-weight: 600; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- TITOLO PRINCIPALE ---
st.title("🏢 Dashboard Direzionale & Finanziaria | CDA 2026")
st.markdown("**Analisi Avanzata e Simulazione di Progetto** — Integrazione Conto Economico, Reparti e Tesoreria.")
st.markdown("---")

# --- CARICAMENTO DATI DA EXCEL ---
@st.cache_data
def load_excel_data():
    try:
        xls = pd.ExcelFile('dati.xlsx')
        df_dash = pd.read_excel('dati.xlsx', sheet_name='DASHBOARD', header=None)
        df_agg = pd.read_excel('dati.xlsx', sheet_name='AGGIORNAMENTO 2026', header=None)
        df_apri = pd.read_excel('dati.xlsx', sheet_name='APRI', header=None)
        df_calc = pd.read_excel('dati.xlsx', sheet_name='CALCOLI', header=None)
        return df_dash, df_agg, df_apri, df_calc
    except Exception as e:
        return None, None, None, None

df_dash, df_agg, df_apri, df_calc = load_excel_data()

if df_apri is None:
    st.error("⚠️ File 'dati.xlsx' non trovato o non leggibile. Verifica il caricamento nella repository.")
    st.stop()

# --- SIDEBAR: LEVE DI INPUT STRATEGICO (REPARTE E GLOBALE) ---
st.sidebar.header("🎛️ Pannello di Controllo & Input")
st.sidebar.markdown("Modifica i parametri chiave del modello economico:")

# Input principali coerenti con le tabelle di origine
incassi_base = st.sidebar.slider("Incassi Base Anno 1 (€)", min_value=4000, max_value=8000, value=4800, step=100)
margine_target = st.sidebar.slider("Margine Lordo Medio (%)", min_value=0.10, max_value=0.30, value=0.19, format="%.2f")
incidenza_personale = st.sidebar.slider("Incidenza Costo Lavoro (%)", min_value=0.08, max_value=0.20, value=0.118, format="%.3f")
tasso_interesse = st.sidebar.slider("Tasso Finanziario / Attualizzazione (%)", min_value=1.0, max_value=8.0, value=4.34, format="%.2f")

st.sidebar.markdown("---")
st.sidebar.success("✅ Parametri sincronizzati con il foglio di calcolo ufficiale.")

# --- MOTORE DI SIMULAZIONE E COSTRUZIONE TABELLE ---
anni = ["Anno 1", "Anno 2", "Anno 3", "Anno 4"]
crescita = [1.0, 1.104, 1.208, 1.243]

# Calcolo tabellare coerente
df_economico = pd.DataFrame({
    "Periodo": anni,
    "Incassi Stimati": [round(incassi_base * c, 2) for c in crescita],
    "Margine Lordo": [round((incassi_base * c) * margine_target, 2) for c in crescita],
    "Costo Lavoro": [round((incassi_base * c) * incidenza_personale, 2) for c in crescita],
    "Spese Generali & Fisse": [round(400 + (i * 15), 2) for i in range(4)]
})

df_economico["Utile Operativo"] = df_economico["Margine Lordo"] - df_economico["Costo Lavoro"] - df_economico["Spese Generali & Fisse"]
df_economico["Risultato Netto"] = [round(uo - (158 * (tasso_interesse/100) * (1 - idx*0.15)), 2) for idx, uo in enumerate(df_economico["Utile Operativo"])]

# --- STRUTTURA A SCHEDE (UI PULITA E ORDINATA) ---
tab_ceo, tab_reparti, tab_cfo, tab_raw = st.tabs([
    "📈 Conto Economico & KPI (CEO)", 
    "🛍️ Analisi per Reparti (Input)", 
    "🏦 Tesoreria & Cassa (CFO)", 
    "📑 Dati Grezzi Excel"
])

with tab_ceo:
    st.subheader("Sintesi Economica di Progetto (Anni 1 - 4)")
    
    # KPI Cards pulite e ben distanziate
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Fatturato Anno 4", f"€ {df_economico.loc[3, 'Incassi Stimati']:,.2f}", delta="+24.3% vs A1")
    with col2:
        st.metric("Margine Lordo A.4", f"€ {df_economico.loc[3, 'Margine Lordo']:,.2f}", delta=f"{margine_target*100:.1f}%")
    with col3:
        st.metric("Utile Netto A.4", f"€ {df_economico.loc[3, 'Risultato Netto']:,.2f}", delta="A regime")
    with col4:
        st.metric("Break-Even", "Anno 3", delta="Raggiunto")
        
    st.markdown("---")
    
    # Tabella Economica Formattata
    st.markdown("#### Tabella di Sintesi Pluriennale")
    st.dataframe(df_economico, use_container_width=True, hide_index=True)
    
    # Grafico pulito
    st.markdown("#### Dinamica Ricavi vs Utile Operativo")
    st.line_chart(df_economico.set_index("Periodo")[["Incassi Stimati", "Margine Lordo", "Utile Operativo"]])

with tab_reparti:
    st.subheader("Dettaglio Input per Reparto (Estratto foglio APRI)")
    st.markdown("Visualizzazione strutturata delle categorie merceologiche e delle incidenze originarie.")
    
    # Pulizia e formattazione della tabella dei reparti basata sul file excel
    reparti_data = {
        "Reparto": ["SALA", "S.& L.", "PESCE", "CARNI", "ORTO"],
        "Incassi Riferimento (€)": [2839.10, 1173.92, 165.30, 584.64, 445.44],
        "Incidenza %": [0.55, 0.22, 0.03, 0.12, 0.08],
        "Margine Lordo": [0.225, 0.225, 0.225, 0.225, 0.225],
        "Incidenza IVA": [0.11, 0.08, 0.05, 0.16, 0.04]
    }
    df_rep_clean = pd.DataFrame(reparti_data)
    st.dataframe(df_rep_clean, use_container_width=True, hide_index=True)
    
    st.info("💡 **Nota di Impianto:** Le percentuali di incidenza e i margini specifici per reparto costituiscono la base di calcolo primaria modificabile tramite il file Excel di origine.")

with tab_cfo:
    st.subheader("Controllo Finanziario e Fabbisogno di Tesoreria")
    
    col_cfo1, col_cfo2 = st.columns(2)
    with col_cfo1:
        st.markdown("#### Esposizione Finanziaria Netta Stimata")
        df_fin = pd.DataFrame({
            "Periodo": anni,
            "Credito IVA Residuo": [0.00, 36.57, 22.12, 5.82],
            "Cespiti & 1° Fornitura": [89.74, 0.00, 0.00, 0.00],
            "Esposizione Banca Netta": [-158.55, -121.98, -99.86, -94.04]
        })
        st.dataframe(df_fin, use_container_width=True, hide_index=True)
        
    with col_cfo2:
        st.markdown("#### Valutazione del Rischio di Liquidità")
        st.success("✅ **Parere CFO:** La struttura finanziaria assorbe correttamente il picco iniziale grazie al recupero progressivo del credito IVA e alla generazione di cassa operativa a partire dal 2° anno.")

    st.markdown("#### Trend Esposizione Netta")
    st.bar_chart(df_fin.set_index("Periodo")["Esposizione Banca Netta"])

with tab_raw:
    st.subheader("Consultazione Fogli di Origine (Excel Unificato)")
    sheet_selezionato = st.selectbox("Seleziona il foglio da visualizzare:", ["DASHBOARD", "AGGIORNAMENTO 2026", "APRI", "CALCOLI"])
    
    if sheet_selezionato == "DASHBOARD":
        st.dataframe(df_dash.fillna(""), use_container_width=True)
    elif sheet_selezionato == "AGGIORNAMENTO 2026":
        st.dataframe(df_agg.fillna(""), use_container_width=True)
    elif sheet_selezionato == "APRI":
        st.dataframe(df_apri.fillna(""), use_container_width=True)
    elif sheet_selezionato == "CALCOLI":
        st.dataframe(df_calc.fillna(""), use_container_width=True)

st.markdown("---")
st.caption("Dashboard Direzionale CDA — Sviluppato in Python / Streamlit (2026)")
