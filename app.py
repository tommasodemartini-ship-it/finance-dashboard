import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione Categorie basata sui tuoi file
CATEGORIES = {
    'Stipendio': ['DECATHLON'],
    'Affitto/Casa': ['ALQUILER', 'AIGUES', 'BONPREU', 'DIGI', 'IKEA', 'LEROY MERLIN', 'HERSAN'],
    'Auto': ['RATA MACCHINA', 'PARKING', 'VERTI', 'TELPARK', 'TUNELSPAN'],
    'Spesa': ['MERCADONA', 'CAPRABO', 'ALCAMPO', 'DIA', 'BON PREU', 'SPAR'],
    'Uscite/Food': ['MATIENZO', 'KFC', 'RISTORANTE', 'PIBA', 'RESTAURANTE', 'MCDONALDS', 'CAFETERIA'],
    'Viaggi': ['EASYJET', 'GOTOGATE', 'AENA'],
    'Sport': ['WELLHUB', 'DUET SPORTS'],
    'Abbonamenti': ['NETFLIX', 'AMAZON PRIME', 'TIMELEFT']
}

INTERNAL_TRANSFERS = ['REVOLUT', 'TOMMASO DE MARTINI', 'RICARICA']

def categorizer(concept):
    concept = str(concept).upper()
    if any(k in concept for k in INTERNAL_TRANSFERS):
        return 'Giroconto/Investimento'
    for cat, keywords in CATEGORIES.items():
        if any(k in concept for k in keywords):
            return cat
    return 'Altro'

st.set_page_config(page_title="Tommaso Money Flow", layout="wide")
st.title("📊 Dashboard Finanziaria Tommaso")

# Sidebar per caricamento
uploaded_file = st.sidebar.file_uploader("Carica l'estratto conto (BBVA o Revolut)", type=['csv', 'xlsx'])

if uploaded_file:
    # Lettura e processamento (Logica per BBVA [F.Oper, Concepto, Importe])
    df = pd.read_csv(uploaded_file) 
    df['Categoria'] = df['Concepto'].apply(categorizer)
    
    # Metriche
    income = df[(df['Importe'] > 0) & (df['Categoria'] != 'Giroconto/Investimento')]['Importe'].sum()
    expenses = df[(df['Importe'] < 0) & (df['Categoria'] != 'Giroconto/Investimento')]['Importe'].abs().sum()
    savings = income - expenses
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Entrate Reali", f"€{income:,.2f}")
    c2.metric("Spese Reali", f"€{expenses:,.2f}")
    c3.metric("Risparmio Netto", f"€{savings:,.2f}")

    # Grafico Patrimonio Globale
    st.subheader("📈 Andamento Patrimonio (Conto + Risparmi)")
    df['Patrimonio'] = df['Saldo'].ffill() 
    fig_line = px.line(df, x='F.Oper', y='Patrimonio', title="Evoluzione Ricchezza")
    st.plotly_chart(fig_line, use_container_width=True)

    # Grafico Spese
    st.subheader("🍕 Distribuzione Spese")
    df_exp = df[(df['Importe'] < 0) & (df['Categoria'] != 'Giroconto/Investimento')]
    fig_pie = px.pie(df_exp, values=df_exp['Importe'].abs(), names='Categoria', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)
