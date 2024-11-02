import streamlit as st

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
    st.header("Resultados do NPS")
    # Coloque o conteúdo protegido aqui
    st.write("Aqui estão os resultados do NPS.")
