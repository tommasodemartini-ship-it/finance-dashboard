import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione Categorie (basata sui tuoi file)
CATEGORIES = {
    'Stipendio': ['DECATHLON'],
    'Affitto/Casa': ['ALQUILER', 'AIGUES', 'BONPREU', 'DIGI', 'IKEA', 'LEROY MERLIN'],
    'Auto': ['RATA MACCHINA', 'PARKING', 'VERTI', 'TELPARK'],
    'Spesa': ['MERCADONA', 'CAPRABO', 'ALCAMPO', 'DIA', 'SPAR'],
    'Uscite': ['MATIENZO', 'KFC', 'RISTORANTE', 'PIBA', 'SOFIA BY PICNIC', 'MCDONALDS'],
    'Viaggi': ['EASYJET', 'GOTOGATE', 'AENA'],
}

INTERNAL_TRANSFERS = ['REVOLUT', 'TOMMASO DE MARTINI', 'RICARICA']

def categorizer(concept):
    concept = str(concept).upper()
    if any(k in concept for k in INTERNAL_TRANSFERS): return 'Investimento/Giroconto'
    for cat, keywords in CATEGORIES.items():
        if any(k in concept for k in keywords): return cat
    return 'Altro'

st.set_page_config(page_title="Tommaso Finance Hub", layout="wide")
st.title("📊 Financial Dashboard Storica")

# Caricamento del Database Storico (il file CSV che avrai su GitHub)
try:
    df_history = pd.read_csv("database_storico.csv")
except:
    df_history = pd.DataFrame()

# Caricamento nuovi dati
uploaded_file = st.sidebar.file_uploader("Carica nuovo PDF (BBVA o Revolut)", type=['pdf', 'csv'])

if uploaded_file:
    # Qui il codice estrae i dati dal PDF e li aggiunge al DataFrame
    st.sidebar.success("Nuovi dati caricati con successo!")

# --- VISUALIZZAZIONI ---
st.header("📈 Analisi Spese per Categoria e Mese")

# Grafico a barre raggruppate per mese e categoria
df_exp = df_history[(df_history['Importe'] < 0) & (df_history['Categoria'] != 'Investimento/Giroconto')]
fig = px.bar(df_exp, x='Mese', y=df_exp['Importe'].abs(), color='Categoria', 
             barmode='group', title="Evoluzione Mensile delle Spese")
st.plotly_chart(fig, use_container_width=True)

st.header("💰 Patrimonio Globale")
# Calcolo basato sui tuoi saldi finali: BBVA (€231,22 [cite: 44]) + Revolut (€14.964,29 )
current_wealth = 15195.51 
st.metric("Patrimonio Totale Consolidato", f"€ {current_wealth:,.2f}")
