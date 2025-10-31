import streamlit as st
import utils
import pandas as pd

st.set_page_config(
    page_title="Calendario",
    page_icon="🗓️",
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

# --- Lógica de la Página ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Debes iniciar sesión para ver el calendario.")
    st.page_link("1_🏛️_Campus_Digital.py", label="Ir a la página de inicio", icon="🏛️")
else:
    st.sidebar.button("Cerrar Sesión", on_click=utils.logout, type="primary")
    st.title("🗓️ Calendario Unificado")
    st.write("Aquí puedes ver todas tus fechas importantes: clases en vivo, fechas límite y tutorías.")
    
    events = utils.get_all_calendar_events()
    
    if not events:
        st.info("No hay eventos en el calendario.")
    else:
        # Convertir a DataFrame de Pandas para mejor visualización
        try:
            df = pd.DataFrame(events)
            
            # Unir con nombres de cursos para claridad
            courses = utils.get_all_courses()
            courses_df = pd.DataFrame(courses)[['course_id', 'title']]
            courses_df = courses_df.rename(columns={'title': 'Curso'})
            
            df = pd.merge(df, courses_df, on='course_id', how='left')
            df['Curso'] = df['Curso'].fillna('General')
            
            # Formatear
            df = df.rename(columns={
                'title': 'Evento',
                'event_date': 'Fecha',
                'event_type': 'Tipo'
            })
            
            # Reordenar columnas
            df = df[['Fecha', 'Evento', 'Tipo', 'Curso']]
            
            # Ordenar por fecha
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df = df.sort_values(by='Fecha')
            
            st.write("### Próximos Eventos")
            
            # Usar st.data_editor para una vista de tabla moderna
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Fecha": st.column_config.DatetimeColumn(
                        "Fecha",
                        format="YYYY-MM-DD HH:mm",
                    )
                }
            )

        except Exception as e:
            st.error(f"No se pudo mostrar el calendario: {e}")
            st.json(events) # Mostrar datos crudos en caso de error
