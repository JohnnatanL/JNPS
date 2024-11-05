import streamlit as st
import re
from bd import insert_data

# Inicialização do session_state
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'selected_score' not in st.session_state:
    st.session_state.selected_score = None

# Função para criar estilo do botão
def get_button_style(score):
    if st.session_state.selected_score == score:
        return {"backgroundColor": "#0066cc", "color": "white"}
    return {}

# Função para atualizar a nota selecionada
def update_score(score):
    st.session_state.selected_score = score
    st.session_state.nota = str(score)

# Inicialização da nota no session_state
if 'nota' not in st.session_state:
    st.session_state.nota = ""

st.header("🌟 Pesquisa NPS")

col_nome, col_email = st.columns(2)
with col_nome:
    nome = st.text_input("Seu Nome")

# Validação do número de telefone
def validate_phone(phone):
    numbers_only = re.sub(r'[^0-9]', '', phone)
    if not numbers_only:
        return False, "Por favor, digite um número de telefone"
    if len(numbers_only) < 10 or len(numbers_only) > 11:
        return False, "Número inválido. Digite um número com DDD (ex: 11999999999)"
    ddd = numbers_only[:2]
    if not (10 <= int(ddd) <= 99):
        return False, "DDD inválido"
    if len(numbers_only) == 11 and numbers_only[2] != '9':
        return False, "Celular deve começar com 9"
    return True, "Número válido!"

def format_phone(phone):
    numbers_only = re.sub(r'[^0-9]', '', phone)
    if len(numbers_only) == 11:
        return f"({numbers_only[:2]}) {numbers_only[2:7]}-{numbers_only[7:]}"
    elif len(numbers_only) == 10:
        return f"({numbers_only[:2]}) {numbers_only[2:6]}-{numbers_only[6:]}"
    return phone

if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ""
if 'phone_valid' not in st.session_state:
    st.session_state.phone_valid = False
if 'validation_message' not in st.session_state:
    st.session_state.validation_message = ""

def on_phone_change():
    is_valid, message = validate_phone(st.session_state.phone_input)
    st.session_state.phone_valid = is_valid
    st.session_state.validation_message = message
    if is_valid:
        st.session_state.phone_number = format_phone(st.session_state.phone_input)
    else:
        st.session_state.phone_number = st.session_state.phone_input

with col_email:
    phone_input = st.text_input(
        "WhatsApp",
        key="phone_input",
        value=st.session_state.phone_number,
        on_change=on_phone_change,
        placeholder="(11) 99999-9999"
    )

if st.session_state.validation_message:
    if st.session_state.phone_valid:
        st.success(st.session_state.validation_message)
    else:
        st.error(st.session_state.validation_message)

st.write("Em uma escala de 0 a 10, qual é a probabilidade de você recomendar a nossa cafeteria para um amigo ou colega?")

cola, colb = st.columns(2)
with cola:
    col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(11)

buttons_config = [
    (col0, "😢 0", 0),
    (col1, "😢 1", 1),
    (col2, "😢 2", 2),
    (col3, "😕 3", 3),
    (col4, "😕 4", 4),
    (col5, "😕 5", 5),
    (col6, "😐 6", 6),
    (col7, "😐 7", 7),
    (col8, "🙂 8", 8),
    (col9, "🙂 9", 9),
    (col10, "😄 10", 10)
]

for col, label, score in buttons_config:
    with col:
        st.button(
            label,
            key=f"btn_{score}",
            use_container_width=True,
            type="primary" if st.session_state.selected_score == score else "secondary",
            on_click=update_score,
            args=(score,)
        )

with colb:
    colba, colbb, colbc, colbd, colbe = st.columns(5)

produtos = st.multiselect("Qual café de sua preferência?", options=["Prensa Francesa", "V60", "Coado Tradicional", "Expresso"])

curso = st.selectbox("Você teria interesse em participar de cursos práticos sobre cafés especiais?", options=["Sim, tenho muito interesse.", "Talvez, dependendo do conteúdo.", "Não tenho interesse no momento."])
curso_retorno = ""
comentario = st.text_area("Deixe seu comentário (opcional)")

enviar = st.button("Enviar Resposta")

if enviar and nome and phone_input and st.session_state.phone_valid and st.session_state.nota and curso:
    if curso[:3] == "Sim":
        curso_retorno = "Sim"
    elif curso[:3] == "Tal":
        curso_retorno = "Talvez"
    elif curso[:3] == "Não":
        curso_retorno = "Não"
    insert_data(nome, re.sub(r'[^0-9]', '', st.session_state.phone_number), st.session_state.nota, produtos, comentario, curso_retorno)
    st.success("Resposta enviada com sucesso!")
    
    # Adicionar um flag no session_state para controlar o reset
    if 'should_reset' not in st.session_state:
        st.session_state.should_reset = True
        
elif 'should_reset' in st.session_state and st.session_state.should_reset:
    # Limpar todos os campos
    st.session_state.nome = ""
    st.session_state.phone_number = ""
    #st.session_state.phone_input = ""
    st.session_state.phone_valid = False
    st.session_state.validation_message = ""
    st.session_state.selected_score = None
    st.session_state.nota = ""
    st.session_state.responses = []
    st.session_state.should_reset = False
    
    # Agora sim, recarregar a página
    st.rerun()
