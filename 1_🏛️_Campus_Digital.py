import streamlit as st
import utils  # Nuestro backend
import sqlite3
from contextlib import closing
import os # Importar os para manejo de rutas

# --- Configuración de la Página ---
# Esto debe ser el primer comando de Streamlit
st.set_page_config(
    page_title="Campus Digital - MSc J. Zamora",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Cargar Estilos ---
def load_css():
    """Carga el archivo CSS personalizado."""
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Archivo style.css no encontrado. Asegúrate de que esté en el mismo directorio.")

load_css()

# --- Inicialización de la DB (Solo se ejecuta una vez) ---
# Usamos un archivo 'lock' simple para saber si ya se inicializó
try:
    with open('.db_initialized.lock', 'x') as f:
        pass # El archivo no existía, así que lo creamos y procedemos a inicializar
    
    print("Primera ejecución: Inicializando y poblando la base de datos...")
    try:
        with closing(sqlite3.connect(utils.DB_FILE)) as conn:
            utils.init_db_tables(conn)
            utils.populate_db(conn)
            print("Base de datos inicializada y poblada.")
    except Exception as e:
        print(f"Error inicializando la base de datos: {e}")
        # Si falla, eliminamos el lock para intentarlo de nuevo en la próxima recarga
        import os
        os.remove('.db_initialized.lock')

except FileExistsError:
    # El archivo .db_initialized.lock ya existe, no hacemos nada.
    pass

# --- Función de Callback para Navegación ---
def select_course(course_id, course_title):
    """Guarda el curso seleccionado en el estado de la sesión y navega a la página del curso."""
    st.session_state['current_course_id'] = course_id
    st.session_state['current_course_title'] = course_title
    st.switch_page("pages/2_📚_Mis_Cursos.py")

# --- Lógica de Autenticación ---
def show_login_form():
    """Muestra el formulario de login."""
    # Ruta al logo
    logo_path = "images/logoZ.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=300) # El logo en el formulario de login
    else:
        st.error(f"Logo no encontrado en: {logo_path}. Asegúrate de que el archivo exista.")
        st.image("https://placehold.co/300x100/003366/FFFFFF?text=Logo+J.+Zamora", width=300) # Placeholder si no se encuentra
        
    st.title("Bienvenido al Campus Digital")
    st.write("Por favor, inicia sesión para acceder a tus cursos.")
    
    with st.form("login_form"):
        username = st.text_input("Usuario", placeholder="usuario_demo")
        password = st.text_input("Contraseña", type="password", placeholder="12345")
        submitted = st.form_submit_button("Ingresar")

        if submitted:
            user = utils.check_login(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user['user_id']
                st.session_state['user_name'] = user['full_name']
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

# --- Vista Principal del Campus (Si está logueado) ---
def show_campus():
    """Muestra la página principal del campus."""
    
    # Header del Campus
    st.sidebar.success(f"Sesión iniciada como:\n**{st.session_state['user_name']}**")
    st.sidebar.button("Cerrar Sesión", on_click=logout, type="primary")

    # --- Banner Principal con el Logo ---
    logo_path = "images/logoZ.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True) # El logo como banner principal
    else:
        st.error(f"Logo no encontrado en: {logo_path}. Asegúrate de que el archivo exista.")
        st.image("https://placehold.co/1200x300/004a99/FFFFFF?text=Bienvenido+al+Campus", use_container_width=True) # Placeholder si no se encuentra
        
    st.title(f"🏛️ Campus Digital de {st.session_state['user_name']}")
    
    # --- Mensaje de Bienvenida ---
    st.markdown("""
    <div class="callout">
        <p>¡Hola! 👋 Bienvenido a tu espacio de aprendizaje. Aquí encontrarás todos tus cursos, materiales y recursos. Explora el catálogo y no dudes en contactarme si tienes preguntas.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- Catálogo de Cursos (Vista de Galería) ---
    st.header("📚 Catálogo de Cursos Disponibles")
    st.write("Estos son los cursos disponibles en la plataforma. Haz clic para empezar a aprender.")
    
    courses = utils.get_all_courses()
    
    if not courses:
        st.warning("No hay cursos disponibles en este momento.")
        return

    # Creamos una "galería" usando columnas. 3 columnas por fila.
    cols_per_row = 3
    for i in range(0, len(courses), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(courses):
                course = courses[i + j]
                with cols[j]:
                    # Usamos un st.container() con un nombre de clase CSS para estilizar la tarjeta
                    with st.container(border=True):
                        st.image(course['image_url'], use_container_width=True)
                        st.subheader(course['title'])
                        st.markdown(f"<span class='tag'>{course['category']}</span>", unsafe_allow_html=True)
                        st.write(course['description'][:100] + "...")
                        
                        # Botón que llama al callback para navegar
                        st.button(
                            "Ir al Curso",
                            key=f"course_btn_{course['course_id']}",
                            on_click=select_course,
                            args=(course['course_id'], course['title']),
                            type="primary",
                            use_container_width=True
                        )

    st.divider()

    # --- Footer ---
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #888;">
        © 2025 Jesús David Zamora Thowinsson, M.Sc. Todos los derechos reservados.
    </div>
    """, unsafe_allow_html=True)


# --- Función de Logout ---
def logout():
    """Limpia la sesión y muestra el formulario de login."""
    for key in list(st.session_state.keys()):
        if key != 'page_to_rerun': # Clave interna de streamlit
            del st.session_state[key]
    st.rerun()

# --- Lógica Principal de la Página ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_campus()
else:
    show_login_form()

