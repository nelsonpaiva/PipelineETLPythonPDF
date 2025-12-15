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

