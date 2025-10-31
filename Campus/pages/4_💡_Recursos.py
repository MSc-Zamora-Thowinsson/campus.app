import streamlit as st
import utils

st.set_page_config(page_title="Recursos", page_icon="💡", layout="wide")

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
load_css()

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Debes iniciar sesión para ver los recursos.")
    st.page_link("1_🏛️_Campus_Digital.py", label="Ir a la página de inicio", icon="🏛️")
else:
    st.sidebar.button("Cerrar Sesión", on_click=utils.logout, type="primary")
    st.title("💡 Biblioteca de Recursos")
    st.write("Encuentra aquí datasets, notebooks, lecturas y enlaces recomendados para tus cursos.")
    st.info("Plantilla de recursos: agregar filtros por curso, tipo y etiquetas.")
