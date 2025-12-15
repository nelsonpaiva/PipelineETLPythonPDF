import streamlit as st
import pandas as pd
import psycopg2
import altair as alt

@st.cache_resource
def load_data():
    # Conectar ao banco de dados PostgreSQL
    conn = psycopg2.connect(
        host="dpg-d4nqgfmr433s73ea6ung-a.oregon-postgres.render.com",
        database="db_pdf_python",
        user="db_pdf_python_user",
        password="oGYCz9cKtgBTG1v6RsZ3oyciUMAjihwG"
    )
    
    query = """
    SELECT
        n_nota,
        data_de_pregao,
        qted,
        mercadoria,
        txop,
        tx_corretagem,
        cotacao,
        movimentacao,
        cv
    FROM
        gold_fatura;
    """
    
    df = pd.read_sql(query, conn) ## dataframe
    conn.close()
    return df

df = load_data()

# Convertendo a coluna data_de_pregao para datetime.date para evitar conflitos de tipo
df['data_de_pregao'] = pd.to_datetime(df['data_de_pregao']).dt.date

# Filtros
st.sidebar.header("Filtros")
mercadoria_selecionada = st.sidebar.multiselect(
    "Selecione a Mercadoria:",
    options=df["mercadoria"].unique(),
    default=df["mercadoria"].unique()
)
#st.dataframe(df)

# Cria um seletor de intervalo de datas.
data_selecionada = st.sidebar.date_input(
    "Selecione o intervalo de datas:",
    value=[df["data_de_pregao"].min(), df["data_de_pregao"].max()]
)

# Aplica os filtros ao DataFrame original usando:
# - isin() para mercadorias
# - between() para intervalo de datas
df_filtered = df[(df["mercadoria"].isin(mercadoria_selecionada)) & 
                 (df["data_de_pregao"].between(data_selecionada[0], data_selecionada[1]))]

# Define o título principal da aplicação
st.title("KPIs e Gráficos Financeiros - Gold Fatura")

# Texto explicativo
st.write("Tabela de dados filtrados:")

# Exibe o DataFrame na interface do Streamlit
st.dataframe(df_filtered)

# Soma total da coluna movimentacao
total_movimentacao = df_filtered['movimentacao'].sum()

# Soma total da coluna quantidade (qted)
total_qted = df_filtered['qted'].sum()

# Título da seção de KPIs
st.header("KPIs")

# Cria duas colunas para exibir métricas lado a lado
col1, col2 = st.columns(2)

# Exibe os valores formatados
col1.metric(label="Total Movimentação", value=f"R${total_movimentacao:,.2f}")
col2.metric(label="Total Quantidade (qted)", value=f"{total_qted:,}")

# Título da seção
st.header("Quantidade por Mercadoria")

# Cria um gráfico de barras com Altair
qted_chart = alt.Chart(df_filtered).mark_bar().encode(
    x='mercadoria:N',
    y='qted:Q',
    color='mercadoria:N'
).properties(
    title='Quantidade Total por Mercadoria'
)
# Exibe o gráfico na interface do Streamlit
st.altair_chart(qted_chart, use_container_width=True)

# Título da seção
st.header("Movimentação ao longo do tempo")

# Cria um gráfico de linha
movimentacao_chart = alt.Chart(df_filtered).mark_line().encode(
    x='data_de_pregao:T',
    y='movimentacao:Q',
    color='mercadoria:N'
).properties(
    title='Movimentação por Mercadoria ao Longo do Tempo'
)

# Exibe o gráfico de linha
st.altair_chart(movimentacao_chart, use_container_width=True)
