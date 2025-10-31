import streamlit as st
import os

# --- Configuración de la Página ---
# El título y el icono se mostrarán en la barra lateral de navegación
st.set_page_config(
    page_title="Tu Instructor",
    page_icon="👨‍🏫",
    layout="wide"
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

# --- Estilos CSS para el Banner ---
# Añadimos CSS específico para el banner interactivo
st.markdown("""
<style>
.instructor-banner {
    width: 100%;
    height: 300px; /* Altura del banner, puedes ajustarla */
    background-size: cover;
    background-position: center;
    position: relative;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    text-align: center;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.instructor-banner::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5); /* Superposición oscura para legibilidad */
    border-radius: 10px;
}
.banner-content {
    position: relative; /* Asegura que el texto esté sobre la superposición */
    z-index: 2;
}
.banner-content h1 {
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    color: white;
}
.banner-content p {
    font-size: 1.5rem;
    font-weight: 300;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)


# --- Lógica de la Página ---
def show_instructor_page():
    """Muestra la página dedicada al instructor."""
    
    # --- Banner Interactivo ---
    # CAMBIA ESTA URL por la imagen de banner que desees.
    # Puede ser una URL o una ruta local (ej: "images/mi_banner.png")
    banner_image_url = "https://placehold.co/1200x300/333333/FFFFFF?text=Banner+Profesional"
    
    st.markdown(f"""
    <div class="instructor-banner" style="background-image: url('{banner_image_url}');">
        <div class="banner-content">
            <h1>APRENDIZAJE SIMPLE.<br>ENSEÑANZA EFECTIVA.</h1>
            <p>Soy Jesús David Zamora Thowinsson, M.Sc.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    # --- Sección "Conoce a tu Instructor" ---
    st.subheader(" ") # Un poco de espacio
    
    col1, col2 = st.columns([1, 1]) # Proporción 1:1 como la tenías
    
    with col1:
        # --- Tu Foto ---
        photo_path = "images/Logo2.png" # Ruta a tu foto Logo2.png
        if os.path.exists(photo_path):
            st.image(
                photo_path,
                caption="Jesús David Zamora Thowinsson, M.Sc.",
                use_container_width=True
            )
        else:
            st.warning(f"Tu foto no se encontró en: {photo_path}. Asegúrate de que el archivo exista y se llame 'Logo2.png'.")
            st.image(
                "https://placehold.co/400x400/eeeeee/cccccc?text=Tu+Foto+Aquí",
                caption="Jesús David Zamora Thowinsson, M.Sc.",
                use_container_width=True
            )

    with col2:
        st.title("Jesús David Zamora Thowinsson, M.Sc.")
        st.markdown("""
        - Economista y Administrador Público
        - Especialista en Estadística Aplicada
        - MSc en Gerencia Empresarial
        - MSc en Estadística Aplicada
        """)
        
        # --- Texto de Biografía Justificado ---
        # CORRECCIÓN: Cambiado de st.write a st.markdown(..., unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: justify;">
        Soy Jesús D. Zamora Thowinsson, un profesional apasionado por la intersección entre la economía, la estadística, la tecnología y la Inteligencia Artificial. Estoy convencido de que **la educación es el pilar fundamental para el crecimiento** y el desarrollo.
                    
        Como profesional, he dedicado mi carrera a fusionar la rigurosidad analítica con la aplicación práctica del conocimiento. Mi misión es llevar el análisis de datos y la econometría más allá de la teoría, no solo aplicándolos como herramientas estratégicas, sino **ayudando a definir los estándares de su aprendizaje**.
        
        Este compromiso se materializó en mi participación como experto del sector para el SENA (2023-2024), donde contribuí directamente en la estructura de cualificación de perfiles clave para el catálogo de mercadeo, incluyendo Auxiliares de Servicios Estadísticos, Entrevistadores de Encuestas e Investigaciones de Mercado y Digitadores.
                    
        Con una sólida formación como Economista y Administrador Público, complementada con especializaciones y maestrías en Estadística Aplicada y Gerencia Empresarial, mi enfoque es claro: **democratizar el conocimiento técnico**. Me especializo en transformar datos crudos en estrategias efectivas, utilizando herramientas de vanguardia como R, Python, Power BI y Excel avanzado.
        
        Mi compromiso es cultivar el pensamiento analítico. Creo en la innovación constante y en hacer accesibles las herramientas complejas. Mi enfoque no es solo analizar, sino ser un un verdadero aliado en la construcción de soluciones basadas en datos que impulsen el éxito.
        </div>""", unsafe_allow_html=True)
    
    st.divider()

    # --- Sección de Contacto ---
    st.header("💬 Contacto y Redes")
    st.write("Conéctate y sigue mi trabajo en otras plataformas:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Contacto Directo")
        st.markdown("""
        - **Email:** [thowinsson.ai@gmail.com](mailto:thowinsson.ai@gmail.com)
        - **WhatsApp:** [+57 3182793250](https://wa.me/573182793250)
        """)

    with col2:
        st.subheader("Perfiles Profesionales")
        st.markdown("""
        - **LinkedIn:** [zamora thowinsson](https://www.linkedin.com/in/zamora-thowinsson)
        - **GitHub (Principal):** [MSc-Zamora-Thowinsson](https://github.com/MSc-Zamora-Thowinsson)
        - **GitHub (Secundario):** [jthowinsson](https://github.com/jthowinsson)
        - **RPubs:** [j_zamoraTh](https://rpubs.com/j_zamoraTh)
        """)

    st.divider()
    # --- Footer ---
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #888;">
        © 2025 Jesús David Zamora Thowinsson, M.Sc. Todos los derechos reservados.
    </div>
    """, unsafe_allow_html=True)


# --- Control de Acceso ---
# Verificamos si el usuario está logueado (estado guardado desde la pág. principal)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_instructor_page()
else:
    st.error("Debes iniciar sesión para ver esta página.")
    # Apuntamos al archivo principal de login
    st.page_link("1_🏛️_Campus_Digital.py", label="Ir a la página de inicio de sesión", icon="🏠")

