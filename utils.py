import streamlit as st
import sqlite3
import hashlib # Para hashear contraseñas
from contextlib import closing

# --- Constantes ---
DB_FILE = "campus.db"

# --- Conexión y Setup de DB ---

def get_db_connection():
    """Establece conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Devuelve filas como diccionarios
    return conn

def init_db_tables(conn):
    """Crea las tablas de la base de datos si no existen."""
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT
    );
    CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        image_url TEXT,
        instructor TEXT DEFAULT 'Jesus Zamora Thowinsson',
        course_order INTEGER -- AÑADIMOS ESTA LÍNEA
    );
    CREATE TABLE IF NOT EXISTS modules (
        module_id TEXT PRIMARY KEY,
        course_id TEXT NOT NULL,
        title TEXT NOT NULL,
        module_order INTEGER,
        FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS lessons (
        lesson_id TEXT PRIMARY KEY,
        module_id TEXT NOT NULL,
        title TEXT NOT NULL,
        content_type TEXT,
        content_data TEXT,
        lesson_order INTEGER,
        FOREIGN KEY (module_id) REFERENCES modules (module_id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS progress (
        user_id TEXT NOT NULL,
        lesson_id TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0,
        PRIMARY KEY (user_id, lesson_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS calendar_events (
        event_id TEXT PRIMARY KEY,
        course_id TEXT,
        title TEXT NOT NULL,
        event_date TEXT NOT NULL,
        event_type TEXT,
        FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
    );
    """
    conn.executescript(schema)
    print("Tablas creadas (si no existían).")

def populate_db(conn):
    """Puebla la base de datos con datos de ejemplo."""
    try:
        cursor = conn.cursor()

        # --- Usuario Demo ---
        # Hasheamos la contraseña '12345'
        pwd_hash = hashlib.sha256("12345".encode()).hexdigest()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, password_hash, full_name) VALUES (?, ?, ?, ?)",
                       ('user_01', 'usuario_demo', pwd_hash, 'Estudiante Demo'))

        # --- Cursos ---
        # REEMPLAZAMOS la lista de cursos por la lista completa y en orden
        courses_data = [
            ('stat_001', 'Estadística Aplicada', 'Domina las técnicas estadísticas para la toma de decisiones.', 'Estadística', 'https://placehold.co/600x400/1abc9c/ffffff?text=Estadistica+Aplicada', 'J. Zamora', 1),
            # 2. Economía
            ('econ_001', 'Economía (Macroeconomía y Microeconomía)', 'Principios fundamentales de Microeconomía y Macroeconomía.', 'Economía', 'https://placehold.co/600x400/2ecc71/ffffff?text=Economia', 'J. Zamora', 2),
            # 3. Econometría
            ('ecom_001', 'Econometría', 'Modelos econométricos para el análisis de datos económicos.', 'Econometría', 'https://placehold.co/600x400/3498db/ffffff?text=Econometria', 'J. Zamora', 3),
            # 4. Bioestadística
            ('bio_001', 'Bioestadística', 'Estadística aplicada a las ciencias de la salud y la biología.', 'Estadística', 'https://placehold.co/600x400/9b59b6/ffffff?text=Bioestadistica', 'J. Zamora', 4),
            # 5. Análisis de Datos (Usamos el ID 'ds_001' para mantener las lecciones demo)
            ('ds_001', 'Análisis de Datos', 'Aprende a usar Pandas, NumPy y Matplotlib para analizar datos.', 'Análisis de Datos', 'https://placehold.co/600x400/34495e/ffffff?text=Analisis+de+Datos', 'J. Zamora', 5),
            # 6. Inteligencia Artificial (Usamos el ID 'ai_001' para mantener los eventos demo)
            ('ai_001', 'Inteligencia Artificial', 'Explora los conceptos clave de la IA, Machine Learning y Deep Learning.', 'Inteligencia Artificial', 'https://placehold.co/600x400/e74c3c/ffffff?text=Inteligencia+Artificial', 'J. Zamora', 6),
            # 7. Marketing Digital
            ('mkt_001', 'Marketing Digital', 'Estrategias y herramientas para el marketing en la era digital.', 'Marketing', 'https://placehold.co/600x400/e67e22/ffffff?text=Marketing+Digital', 'J. Zamora', 7),
            # 8. Investigación de Mercados
            ('im_001', 'Investigación de Mercados', 'Metodologías para entender al consumidor y al mercado.', 'Marketing', 'https://placehold.co/600x400/f1c40f/000000?text=Investigacion+de+Mercados', 'J. Zamora', 8),
            # 9. Excel
            ('excel_001', 'Excel (Básico, Intermedio y Avanzado)', 'Desde tablas dinámicas hasta macros, domina Excel.', 'Ofimática', 'https://placehold.co/600x400/27ae60/ffffff?text=Excel', 'J. Zamora', 9),
            # 10. Visualización de Datos
            ('viz_001', 'Visualización de Datos', 'Aprende a contar historias con datos usando Python, RStudio y Power BI.', 'Visualización', 'https://placehold.co/600x400/c0392b/ffffff?text=Visualizacion+de+Datos', 'J. Zamora', 10)
        ]
        # Actualizamos la sentencia INSERT para incluir 7 columnas
        cursor.executemany("INSERT OR IGNORE INTO courses (course_id, title, description, category, image_url, instructor, course_order) VALUES (?, ?, ?, ?, ?, ?, ?)", courses_data)

        # --- Módulos (para ds_001) ---
        modules_data = [
            ('ds_001_m01', 'ds_001', 'Módulo 1: Introducción a Pandas', 1),
            ('ds_001_m02', 'ds_001', 'Módulo 2: Visualización con Matplotlib', 2)
        ]
        cursor.executemany("INSERT OR IGNORE INTO modules (module_id, course_id, title, module_order) VALUES (?, ?, ?, ?)", modules_data)

        # --- Lecciones (para ds_001_m01) ---
        lessons_data = [
            ('ds_001_l01', 'ds_001_m01', 'Lección 1.1: ¿Qué es un DataFrame?', 'video', 'https://www.youtube.com/watch?v=wEAUH2aJv1s', 1),
            ('ds_001_l02', 'ds_001_m01', 'Lección 1.2: Lectura de archivos CSV', 'lectura', '### Cómo leer un archivo CSV\nUsamos `pd.read_csv("archivo.csv")` para cargar datos.', 2),
            ('ds_001_l03', 'ds_001_m01', 'Lección 1.3: Selección de datos (loc, iloc)', 'practica', 'Practica seleccionando filas y columnas de tu DataFrame.', 3),
            ('ds_001_l04', 'ds_001_m02', 'Lección 2.1: Gráficos de Líneas', 'video', 'https://www.youtube.com/watch?v=wEAUH2aJv1s', 1)
        ]
        cursor.executemany("INSERT OR IGNORE INTO lessons (lesson_id, module_id, title, content_type, content_data, lesson_order) VALUES (?, ?, ?, ?, ?, ?)", lessons_data)

        # --- Calendario ---
        calendar_data = [
            ('evt_001', 'ds_001', 'Clase en Vivo: Introducción a Pandas', '2025-11-15T18:00:00', 'Clase en Vivo'),
            ('evt_002', 'ai_001', 'Fecha Límite: Ensayo IA', '2025-11-20T23:59:00', 'Fecha Límite'),
            ('evt_003', None, 'Tutoría General: Dudas de Power BI', '2025-11-18T16:00:00', 'Tutoría')
        ]
        cursor.executemany("INSERT OR IGNORE INTO calendar_events (event_id, course_id, title, event_date, event_type) VALUES (?, ?, ?, ?, ?)", calendar_data)

        conn.commit()
        print("Datos de ejemplo insertados.")
    except Exception as e:
        conn.rollback()
        print(f"Error poblando la base de datos: {e}")

# --- Funciones de Autenticación (con caché) ---

@st.cache_data(ttl=300) # Cache por 5 minutos
def check_login(username, password):
    """Verifica las credenciales del usuario."""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        user = cursor.fetchone()
        return dict(user) if user else None

def logout():
    """Limpia la sesión."""
    for key in list(st.session_state.keys()):
        if key != 'page_to_rerun':
            del st.session_state[key]
    st.rerun()

# --- Funciones de Consulta de Datos (con caché) ---

@st.cache_data(ttl=60)
def get_all_courses():
    """Obtiene todos los cursos del catálogo."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        # CAMBIAMOS 'ORDER BY title' A 'ORDER BY course_order'
        cursor.execute("SELECT * FROM courses ORDER BY course_order")
        courses = cursor.fetchall()
        return [dict(course) for course in courses]

@st.cache_data(ttl=60)
def get_course_details(course_id):
    """Obtiene los detalles de un curso específico."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        course = cursor.fetchone()
        return dict(course) if course else None

# Usamos st.cache_data, pero el progreso del usuario no se cacheará bien.
# Para una app real, el progreso (checkbox) debe ser manejado
# sin caché o con una estrategia de limpieza de caché más inteligente.
# Por simplicidad aquí, cacheamos todo.
@st.cache_data(ttl=15)
def get_course_modules_and_lessons(course_id, user_id):
    """Obtiene la estructura completa (módulos y lecciones) de un curso, con el progreso del usuario."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        
        # 1. Obtener módulos
        cursor.execute("SELECT * FROM modules WHERE course_id = ? ORDER BY module_order", (course_id,))
        modules = cursor.fetchall()
        
        course_structure = []
        for module in modules:
            module_dict = dict(module)
            
            # 2. Obtener lecciones para cada módulo
            cursor.execute("""
                SELECT 
                    l.*, 
                    CASE 
                        WHEN p.completed = 1 THEN 1
                        ELSE 0 
                    END as completed
                FROM lessons l
                LEFT JOIN progress p ON l.lesson_id = p.lesson_id AND p.user_id = ?
                WHERE l.module_id = ?
                ORDER BY l.lesson_order
            """, (user_id, module['module_id']))
            
            lessons = cursor.fetchall()
            module_dict['lessons'] = [dict(lesson) for lesson in lessons]
            course_structure.append(module_dict)
            
        return course_structure

@st.cache_data(ttl=60)
def get_all_calendar_events():
    """Obtiene todos los eventos del calendario."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calendar_events ORDER BY event_date")
        events = cursor.fetchall()
        return [dict(event) for event in events]

# --- Funciones de Escritura de Datos (Sin caché) ---

def update_lesson_progress(user_id, lesson_id, completed_status):
    """Inserta o actualiza el progreso de una lección para un usuario."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO progress (user_id, lesson_id, completed)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, lesson_id) 
                DO UPDATE SET completed = excluded.completed;
            """, (user_id, lesson_id, bool(completed_status)))
            conn.commit()
            
            # Limpiamos el caché de la función que lee el progreso
            # para que los cambios se reflejen
            st.cache_data.clear()
            
        except Exception as e:
            conn.rollback()
            print(f"Error en update_lesson_progress: {e}")
            raise e


