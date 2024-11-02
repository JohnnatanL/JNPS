import streamlit as st

st.set_page_config(
        page_title="Zona de Teste Cafeteria",
        page_icon="☕",
        layout="wide"
    )

nps = st.Page("coffee/nps.py", title="Pesquisa NPS", icon=":material/star:", default=True)
nps_result = st.Page("coffee/nps_result.py", title="Resultado NPS", icon=":material/dashboard:")
perfil_gosto = st.Page("coffee/perfil_gosto.py", title="Perfil de Gosto", icon=":material/dashboard:")

pg = st.navigation(
    {"Área do Cliente": [nps, perfil_gosto],
    "Relatórios": [nps_result],}
)

pg.run()