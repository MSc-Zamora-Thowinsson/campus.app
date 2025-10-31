import streamlit as st
import utils

st.set_page_config(page_title="Comunidad", page_icon="💬", layout="wide")

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
load_css()

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Debes iniciar sesión para ver la comunidad.")
    st.page_link("1_🏛️_Campus_Digital.py", label="Ir a la página de inicio", icon="🏛️")
else:
    st.sidebar.button("Cerrar Sesión", on_click=utils.logout, type="primary")
    st.title("💬 Comunidad")
    st.write("Espacio para anuncios, preguntas generales y redes entre estudiantes.")
    st.info("Plantilla: integrar foros, o enlaces a canales externos (Discord, Slack).")
