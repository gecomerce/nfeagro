import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="NFE-Agro", layout="wide")

card1, card2, card3, card4, card5 = st.columns([1,1,1,1,0.5])

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSm1RPdkTOOGv0LyZme-uF6toj56tKZgWfzQza6E11tAFkZY46c2J3YFSjkQXmy9ub5CHTGxKvSx6OO/pub?gid=0&single=true&output=csv'

@st.cache_data
def load_data():
    df = pd.read_csv(url)
    df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
    df['Data'] = pd.to_datetime(df['Vencimento'], format='%d/%m/%Y', errors='coerce')
    df["Ano"] = df['Data'].dt.year
    df["Mês"] = df['Data'].dt.month
    return df

df = load_data()

# -------------------------------------------------------------------

ano = st.selectbox("Ano", [2025,2024,2023])

df_filtered = df.query('Ano ==@ano')

# -------------------------------------------------------------------


df_filtered
# -------------------------------------------------------------------

total_entrada = df_filtered.loc[df['Tipo'] == 'Entrada', 'Valor'].sum()
qtd_entradas = df_filtered.loc[df_filtered['Tipo'] == 'Entrada', 'Valor'].count()


with card1:
    st.metric("Total Entradas",f'💵 R$ {total_entrada:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

with card2:
    st.metric("QTD Entradas", qtd_entradas)

    
# -------------------------------------------------------------------

df_pie = df_filtered.groupby('Tipo')['Valor'].sum().reset_index()

pie_chart = px.pie(df_pie,names="Tipo", values="Valor")

# -------------------------------------------------------------------


pie_chart

