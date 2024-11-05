import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Define a senha correta (idealmente, use uma variável de ambiente)
PASSWORD = "cafe.10.27"

# Função de autenticação
def check_password():
    st.title("Login")
    password = st.text_input("Senha:", type="password")
    if password == PASSWORD:
        return True
    else:
        st.error("Senha incorreta")
        return False

# Verifica a senha antes de mostrar o conteúdo
if check_password():
    # Carregar variáveis de ambiente
    load_dotenv()
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    conn_info = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': '6543'  # ou a porta do seu banco de dados
    }

    # Função para carregar dados
    @st.cache_data
    def carregar_dados():
        query = "SELECT nome_cliente, whatsapp, nota, produtos_pref, comentarios, interesse_curso FROM cafe.nps_response"
        conn = psycopg2.connect(**conn_info)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        colunas = ['nome_cliente', 'whatsapp', 'nota', 'produtos_pref', 'comentarios', 'interesse_curso']
        df = pd.DataFrame(result, columns=colunas)
        df['nota'] = pd.to_numeric(df['nota'], errors='coerce')
        return df

    # Função para calcular o NPS
    def calcular_nps(df):
        promotores = df[df['nota'] >= 9].shape[0]
        detratores = df[df['nota'] <= 6].shape[0]
        total_respondentes = df.shape[0]
        nps_score = ((promotores - detratores) / total_respondentes) * 100
        return nps_score

    # Carregar dados e calcular NPS
    df = carregar_dados()
    nps_score = calcular_nps(df)

    # Exibir NPS no Streamlit
    st.title("Análise NPS")
    st.metric("NPS Score", f"{nps_score:.2f}")

    # Separar produtos preferidos em colunas individuais
    cafe_tipos = ["Prensa Francesa", "V60", "Coado Tradicional", "Expresso"]
    for cafe in cafe_tipos:
        df[cafe] = df['produtos_pref'].apply(lambda x: cafe in x)

    # Calcular a média das notas para cada tipo de café
    medias_cafe = {}
    for cafe in cafe_tipos:
        medias_cafe[cafe] = df[df[cafe]]['nota'].mean()

    # Exibir preferências de produtos
    st.subheader("Média das Notas por Tipo de Café Preferido")
    media_df = pd.DataFrame.from_dict(medias_cafe, orient='index', columns=['Média da Nota'])
    st.bar_chart(media_df, stack=True)

    # Exibir comentários e produtos preferidos
    st.subheader("Comentários dos Clientes")
    for _, row in df.iterrows():
        cafes_preferidos = [cafe for cafe in cafe_tipos if row[cafe]]
        st.write(f"**{row['nome_cliente']} ({row['whatsapp']})** | {row['comentarios']} | Prefere: {', '.join(cafes_preferidos)} | Interesse no curso: {row['interesse_curso']}")
