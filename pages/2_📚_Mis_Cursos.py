import streamlit as st
import utils
from contextlib import closing

st.set_page_config(
    page_title="Mis Cursos",
    page_icon="📚",
    layout="wide"
)

# Cargar CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
load_css()

# --- Callbacks de Progreso ---
def toggle_lesson_progress(user_id, lesson_id, current_status):
    """Actualiza el estado de 'completado' de una lección en la DB."""
    new_status = not current_status
    print(f"Callback: Toggling lesson {lesson_id} for user {user_id} to {new_status}")
    try:
        utils.update_lesson_progress(user_id, lesson_id, new_status)
        # Forzamos un 'rerun' para que los checkboxes se actualicen visualmente
        # (Aunque el manejo de estado de st.checkbox a veces lo hace automáticamente)
        # st.rerun() # Descomentar si el estado no se refleja
    except Exception as e:
        st.error(f"Error actualizando tu progreso: {e}")

# --- Renderizado de Lecciones ---
def render_lesson_content(lesson):
    """Muestra el contenido de una lección según su tipo."""
    if lesson['content_type'] == 'video':
        st.video(lesson['content_data'])
    elif lesson['content_type'] == 'lectura':
        st.markdown(lesson['content_data'], unsafe_allow_html=True)
    elif lesson['content_type'] == 'practica':
        st.markdown(lesson['content_data'], unsafe_allow_html=True)
        st.code("print('¡Este es un bloque de código de ejemplo!')", language="python")
    else:
        st.write("Contenido de la lección no disponible.")

# --- Vista Principal del Aula ---
def show_course_aula(course_id, user_id):
    """Renderiza la página completa de un curso (Nivel 3)."""
    
    course_details = utils.get_course_details(course_id)
    if not course_details:
        st.error("No se pudieron cargar los detalles del curso.")
        st.page_link("1_🏛️_Campus_Digital.py", label="Volver al Campus", icon="🏛️")
        return

    # --- Header del Curso ---
    st.title(course_details['title'])
    st.image(course_details['image_url'], use_container_width=True)
    st.markdown(f"<span class='tag'>{course_details['category']}</span>", unsafe_allow_html=True)
    st.markdown(course_details['description'])
    
    st.divider()

    # --- Pestañas de Contenido (Tu "Plantilla") ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "**Contenido del Curso (Temario)**",
        "**Proyectos y Evaluaciones**", 
        "**Recursos del Curso**",
        "**Preguntas y Discusión**"
    ])

    # --- Pestaña 1: Contenido del Curso (Temario Interactivo) ---
    with tab1:
        st.header("Temario Interactivo")
        st.write("Aquí puedes ver todos los módulos y lecciones. Marca las casillas a medida que completas cada lección para seguir tu progreso.")
        
        modules = utils.get_course_modules_and_lessons(course_id, user_id)
        
        if not modules:
            st.info("El contenido de este curso se está preparando. ¡Vuelve pronto!")
            return

        total_lessons = sum(len(mod['lessons']) for mod in modules)
        completed_lessons = sum(sum(1 for les in mod['lessons'] if les['completed']) for mod in modules)
        
        progress_percent = 0
        if total_lessons > 0:
            progress_percent = (completed_lessons / total_lessons)
        
        st.progress(progress_percent, text=f"{completed_lessons} de {total_lessons} lecciones completadas")
        st.markdown("---")


        # Iteramos y creamos los "Expanders" para los módulos
        for module in modules:
            with st.expander(f"**{module['title']}**", expanded=module['module_order'] == 1):
                st.write(f"Lecciones del Módulo {module['module_order']}:")
                
                for lesson in module['lessons']:
                    col1, col2 = st.columns([1, 10])
                    
                    with col1:
                        # El checkbox maneja el estado de 'completado'
                        st.checkbox(
                            label="", # Etiqueta vacía, el título lo ponemos en col2
                            value=lesson['completed'],
                            key=f"progress_{lesson['lesson_id']}",
                            on_change=toggle_lesson_progress,
                            args=(user_id, lesson['lesson_id'], lesson['completed']),
                            label_visibility="collapsed"
                        )
                    
                    with col2:
                        # Usamos un 'subheader' para la lección para que se pueda colapsar
                        with st.popover(f"**{lesson['title']}**", use_container_width=True):
                            st.subheader(f"Lección: {lesson['title']}")
                            render_lesson_content(lesson)

    # --- Pestaña 2: Proyectos ---
    with tab2:
        st.header("Proyectos y Evaluaciones")
        st.info("Esta sección aún está en construcción.")
        st.write("Aquí encontrarás tus tareas, quizzes y proyectos finales.")
        # Aquí iría una vista de la DB "Evaluaciones" filtrada por este curso

    # --- Pestaña 3: Recursos ---
    with tab3:
        st.header("Biblioteca de Recursos del Curso")
        st.info("Esta sección aún está en construcción.")
        st.write("Aquí encontrarás datasets, notebooks, artículos y herramientas recomendadas.")
        # Aquí iría una vista de la DB "Biblioteca de Recursos" filtrada por este curso

    # --- Pestaña 4: Discusión ---
    with tab4:
        st.header("Preguntas y Discusión")
        st.write("Usa este espacio para hacer preguntas sobre el contenido del curso.")
        # Streamlit no tiene un sistema de comentarios nativo.
        # Se podría integrar con 'streamlit-disqus' o un formulario que guarde en una DB.
        st.info("Función de comentarios en desarrollo.")
        with st.form("new_question_form"):
            st.text_area("Escribe tu pregunta o comentario:")
            st.form_submit_button("Publicar", disabled=True)


# --- Lógica Principal de la Página ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Debes iniciar sesión para ver tus cursos.")
    st.page_link("1_🏛️_Campus_Digital.py", label="Ir a la página de inicio", icon="🏛️")
else:
    # Verificamos si hay un curso seleccionado en la sesión
    if 'current_course_id' in st.session_state:
        st.sidebar.page_link("1_🏛️_Campus_Digital.py", label="Volver al Campus", icon="🏛️")
        st.sidebar.success(f"Viendo curso:\n**{st.session_state['current_course_title']}**")
        st.sidebar.button("Cerrar Sesión", on_click=utils.logout, type="primary")

        show_course_aula(
            st.session_state['current_course_id'],
            st.session_state['user_id']
        )
    else:
        st.info("No has seleccionado ningún curso.")
        st.page_link("1_🏛️_Campus_Digital.py", label="Ir al Catálogo de Cursos", icon="🏛️")
