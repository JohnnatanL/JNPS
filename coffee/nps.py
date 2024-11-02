import streamlit as st
import re
from bd import insert_data

#st.set_page_config(page_title="Pesquisa NPS", layout="wide")

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
def validate_phone(phone):
    # Remove todos os caracteres não numéricos
    numbers_only = re.sub(r'[^0-9]', '', phone)
    
    # Verifica se o número está vazio
    if not numbers_only:
        return False, "Por favor, digite um número de telefone"
    
    # Verifica se o número tem entre 10 e 11 dígitos (com DDD)
    if len(numbers_only) < 10 or len(numbers_only) > 11:
        return False, "Número inválido. Digite um número com DDD (ex: 11999999999)"
    
    # Verifica se começa com DDD válido (assumindo DDDs do Brasil)
    ddd = numbers_only[:2]
    if not (10 <= int(ddd) <= 99):
        return False, "DDD inválido"
    
    # Se tiver 11 dígitos, verifica se o primeiro dígito após DDD é 9
    if len(numbers_only) == 11 and numbers_only[2] != '9':
        return False, "Celular deve começar com 9"
    
    return True, "Número válido!"

def format_phone(phone):
    # Remove todos os caracteres não numéricos
    numbers_only = re.sub(r'[^0-9]', '', phone)
    
    if len(numbers_only) == 11:
        return f"({numbers_only[:2]}) {numbers_only[2:7]}-{numbers_only[7:]}"
    elif len(numbers_only) == 10:
        return f"({numbers_only[:2]}) {numbers_only[2:6]}-{numbers_only[6:]}"
    return phone

# Inicializa o estado para o número de telefone se não existir
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = ""
if 'phone_valid' not in st.session_state:
    st.session_state.phone_valid = False
if 'validation_message' not in st.session_state:
    st.session_state.validation_message = ""

def on_phone_change():
    # Valida e formata o número quando o input muda
    is_valid, message = validate_phone(st.session_state.phone_input)
    st.session_state.phone_valid = is_valid
    st.session_state.validation_message = message
    if is_valid:
        st.session_state.phone_number = format_phone(st.session_state.phone_input)
    else:
        st.session_state.phone_number = st.session_state.phone_input

# Cria o input com validação
with col_email:
    phone_input = st.text_input(
        "WhatsApp",
        key="phone_input",
        value=st.session_state.phone_number,
        on_change=on_phone_change,
        placeholder="(11) 99999-9999"
    )

# Mostra mensagem de validação com cores diferentes
if st.session_state.validation_message:
    if st.session_state.phone_valid:
        st.success(st.session_state.validation_message)
    else:
        st.error(st.session_state.validation_message)

# Se quiser acessar o número válido em outro lugar do código:
if st.session_state.phone_valid:
    number_only = re.sub(r'[^0-9]', '', st.session_state.phone_number)

st.write("Como você avalia nossa empresa?")

cola, colb = st.columns(2)
with cola:
    col0, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(11)

# Definição dos botões com emojis e estilos
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

# Criação dos botões com estados persistentes
for col, label, score in buttons_config:
    with col:
        if st.button(
            label,
            key=f"btn_{score}",
            use_container_width=True,
            type="primary" if st.session_state.selected_score == score else "secondary",
            on_click=update_score,
            args=(score,)
        ):
            pass

with colb:
    colba, colbb, colbc, colbd, colbe = st.columns(5)

produtos = st.multiselect("Qual café de sua preferência?", options=["Cerrado", "100% Arábica", "Mogiana", "Expresso", "Tradicional", "Extraforte"])

comentario = st.text_area("Deixe seu comentário (opcional)")

enviar = st.button("Enviar Resposta")

if enviar and nome and phone_input and st.session_state.validation_message == "Número válido!" and score:
    insert_data(nome, number_only, score, produtos, comentario)