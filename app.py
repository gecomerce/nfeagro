import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="NFE-Agro", layout="wide")


card_title, = st.columns(1)
card1, card2, card3, card4, card5 = st.columns([1,1,1,1,0.5])
col1, col2, col3 = st.columns(3)
card_colunas, = st.columns(1)
card_dataframe, = st.columns(1)

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSm1RPdkTOOGv0LyZme-uF6toj56tKZgWfzQza6E11tAFkZY46c2J3YFSjkQXmy9ub5CHTGxKvSx6OO/pub?gid=0&single=true&output=csv'

@st.cache_data
def load_data():
    df = pd.read_csv(url)
    df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
    df['Data'] = pd.to_datetime(df['Vencimento'], format='%d/%m/%Y', errors='coerce')
    df["Ano"] = df['Data'].dt.year
    df["Mês"] = df['Data'].dt.month
    df["Mês"] = df['Mês'].replace({
    1:"Jan",
    2:"Fev",
    3:"Mar",
    4:"Abr",
    5:"Mai",
    6:"Jun",
    7:"Jul",
    8:"Ago",
    9:"Set",
    10:"Out",
    11:"Nov",
    12:"Dez"
    })
    df = df.drop(columns=["Data"])
    return df

df = load_data()



# -------------------------------------------------------------------

with card5:
    ano = st.selectbox("Ano", [2025,2024])

df_filtered = df.query('Ano ==@ano')

with card_title:
    st.title(f'NFe-Agro Visão Financeira {ano} 💰',anchor= False)
# -------------------------------------------------------------------

total_entrada = df_filtered.loc[df['Tipo'] == 'Entrada', 'Valor'].sum()
qtd_entradas = df_filtered.loc[df_filtered['Tipo'] == 'Entrada', 'Valor'].count()

total_saidas = df_filtered.loc[df['Tipo'] == 'Saída', 'Valor'].sum()
qtd_saidas = df_filtered.loc[df_filtered['Tipo'] == 'Saída', 'Valor'].count()


with card1:
    st.metric("Total Entradas",f'💵 R$ {total_entrada:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

with card2:
    st.metric("QTD Entradas", qtd_entradas)

with card3:
    st.metric("Total Saídas",f'💵 R$ {total_saidas:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

with card4:
    st.metric("QTD Saídas", qtd_saidas)

# -------------------------------------------------------------------


df_pie = df_filtered.groupby('Tipo')['Valor'].sum().reset_index()

pie_chart = px.pie(
    df_pie,
    names="Tipo",
    values="Valor",
    title="Por Tipo",
    color="Tipo",
    color_discrete_map={
        "Entrada": "#16a34a",
        "Saída": "#dc2626" 
    }
)

pie_chart.update_traces(
    textposition='inside',
    textinfo='label+percent',
    insidetextfont=dict(color='white', size=14)
)
pie_chart.update_layout(
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title=dict(font=dict(size=18, color='white')),
    legend=dict(visible= False)
)


# ----------------------------------------------------------------
# BARRA CENTRO DE CUSTO

df_centro_de_custo = df_filtered.groupby('Centro de Custo')['Valor'].sum().reset_index()
df_centro_de_custo = df_centro_de_custo.sort_values(by="Valor",ascending=True)
bar_centro_de_custo = px.bar(df_centro_de_custo,x="Valor", y="Centro de Custo",
                             title= "Por Centro de Custo", orientation="h",
                             color_discrete_sequence=["#1351D8"])

bar_centro_de_custo.update_traces(text=df_centro_de_custo["Valor"].apply(
        lambda v: f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ), textposition='auto', textfont=dict(color="white"))

bar_centro_de_custo.update_layout(
    height=400,
    margin=dict(l=110, r=10, t=100, b=40),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title=dict(font=dict(size=18, color='white')),
    xaxis=dict(visible=False),
    yaxis=dict(color='white', title=""),
    showlegend=False
)

# --------------------------------------------------------------------------

df_categoria = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
df_categoria = df_categoria.sort_values(by="Valor", ascending=True)

bar_categoria = px.bar(df_categoria,x="Valor",y="Categoria",
    text=df_categoria["Valor"].apply(
    lambda v: f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    ,title="Por Categoria",orientation="h",color_discrete_sequence=["#1351D8"])

bar_categoria.update_traces(
    textposition='auto',
    textfont=dict(color="white", size=12) 
)

bar_categoria.update_layout(
    height=2200,
    margin=dict(l=110, r=0, t=60, b=40),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title=dict(font=dict(size=18, color='white')),
    xaxis=dict(
        visible=False,
        title="Valor (R$)",
        showgrid=False,
        zeroline=False,
        color='white',
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title=" ",
        showgrid=False,
        automargin=False,
        color='white',
        tickfont=dict(color='white')
    ),
    showlegend=False
)

# -------------------------------------------------------------------

df_colunas = df_filtered.groupby(["Mês","Tipo"])["Valor"].sum().reset_index()
ordem_meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
df_colunas["Mês"] = pd.Categorical(df_colunas["Mês"], categories=ordem_meses, ordered=True)
df_colunas = df_colunas.sort_values("Mês")



bar_colunas = px.bar(
    df_colunas,
    x="Mês",
    color= "Tipo",
    y="Valor",barmode="group",
    text=df_colunas["Valor"].apply(
        lambda v: f"R$ {v:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ),
    title="Movimentação Mensal",
    orientation="v",
        color_discrete_map={
        "Entrada": "#16a34a",
        "Saída": "#dc2626" 
    }
)

bar_colunas.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title=dict(font=dict(size=18, color='white')),
    xaxis=dict(visible=True),
    yaxis=dict(visible=False),
    showlegend=False
)

bar_colunas.update_traces(
    textposition='outside'
)


# -------------------------------------------------------------------

with col1:
    st.plotly_chart(pie_chart, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})


with col2:
    st.plotly_chart(bar_centro_de_custo, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

with col3:
    bar_html = bar_categoria.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False, 'staticPlot': True})
    components.html(
        f"""
        <div style="height:400px; width:350px; margin:0; padding:0; overflow-y:auto;">
            {bar_html}
        </div>
        """,
        height=420,
    )
with card_colunas:
    st.plotly_chart(bar_colunas, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

with card_dataframe:
    mes = st.selectbox("Mês", df_filtered["Mês"].unique())
    df_filtered = df_filtered.query('Mês == @mes')
    df_filtered = df_filtered.drop(columns=["Mês","Ano"])
    st.subheader(f"Movimentações de {mes} de {ano}",anchor= False)
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

#-----------------------------------------------------------------------------------------------------
#estilizacao

borda = """
            <style>
            [data-testid="stColumn"]
            {
            background-color: #000000;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            color: #ffffff;
            opacity: 100%;
            }
            </style>
            """

st.markdown(borda, unsafe_allow_html=True)  