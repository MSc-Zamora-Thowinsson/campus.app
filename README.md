# Arquitectura Técnica del Campus Digital en Streamlit

Este documento traduce la arquitectura de información (IA) y la visión de experiencia de usuario (UX) del "Campus Digital de Jesus Zamora Thowinsson" a una implementación técnica realista y escalable utilizando el framework Streamlit.

1. **Filosofía de Implementación en Streamlit**

La visión de UX se basa en una "Única Fuente de Verdad" (bases de datos relacionales). En Streamlit, esto se traduce de la siguiente manera:
- **Streamlit es el Frontend (La Vista)**: Es la capa de interfaz de usuario, responsable de mostrar el contenido, gestionar la interacción y manejar el estado de la sesión del usuario.
- **La Base de Datos es el Backend (El Modelo)**: La "única fuente de verdad" (Cursos, Lecciones, Usuarios, etc.) **no vive en Streamlit**. 
- Reside en una base de datos externa. Para este prototipo, usaremos SQLite (un solo archivo `campus.db`), pero este diseño es 100% escalable a un sistema más robusto como **Supabase**, **PostgreSQL** o **Firebase**. sin cambiar la lógica de la UI.
- **El** `utils.py` **es el Controlador**: Un conjunto de funciones que conectan el Frontend (Streamlit) con el Backend (DB), gestionan la lógica de negocio (ej. `get_user_courses()`) y se optimizan con el caché de Streamlit.

2. **El "Traductor" de Conceptos (Tu Visión a Streamlit)**

Así es como implementamos tu arquitectura de IA:

|**Concepto de tu Brief (inspirado en Notion/CMS)**||Implementación en Streamlit (Técnica).|
|**Bases de Datos Relacionales (Cursos, Lecciones...)**||Tablas en una base de datos SQLite (`campus.db`).|
|**"Relación" entre bases de datos**||**Claves Foráneas (Foreign Keys)** en el esquema de la base de datos.|
|**"Vistas Enlazadas" y "Filtros"**||**Consultas SQL** (ej. `SELECT * FROM lessons WHERE course_id = ?`) ejecutadas en utils.py.|
|**Páginas (Nivel 1, 2, 3)**||**Aplicación Multipage de Streamlit (archivos .py en la raíz y en la carpeta `/pages`).|
|**"Plantilla de Curso" (Nivel 3)**||Una función de Python (`def render_course_page(course)`) que genera la página dinámicamente usando `st.tabs`, `st.expander` y `st.markdown`.| 
|**Estado del Estudiante (Qué curso mira, progreso)**||`st.session_state`. Es un diccionario persistente para la sesión de cada usuario.|
|**Consistencia de Marca (Branding)**||Un archivo `.streamlit/config.toml` para colores y un `style.css` para tipografía y detalles.|
|**Navegación (Barra Sincronizada)**||La **barra lateral de navegación** que Streamlit crea automáticamente a partir de la estructura de archivos.|

3. **Arquitectura de Archivos (Estructura del Proyecto)**

Esta estructura crea la navegación de tu campus automáticamente.
/ (Campus Digital)
│
├── .streamlit/
│   └── config.toml         # Branding: Colores, fuentes base
│
├── pages/
│   ├── 2_📚_Mis_Cursos.py    # Nivel 3: El Aula Virtual (Plantilla de Curso)
│   ├── 3_🗓️_Calendario.py   # Nivel 2: Vista de Calendario
│   ├── 4_💡_Recursos.py     # Nivel 2: Biblioteca de Recursos
│   └── 5_💬_Comunidad.py    # Nivel 2: Espacio de Comunidad
│
├── 1_🏛️_Campus_Digital.py   # Nivel 1: Página Principal (Login y Catálogo)
├── utils.py                # Lógica de backend: Conexión a DB, queries, auth
├── style.css               # Branding: Estilos CSS personalizados
├── campus.db               # La Base de Datos Relacional (SQLite)
└── README.md               # Este documento

4. **Diseño de la Base de Datos Relacional (Esquema SQL)**

Este es el corazón de tu sistema, implementado en SQLite.

-- Tabla de Cursos (Tu DB 📚 Cursos)
CREATE TABLE IF NOT EXISTS courses (
    course_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    image_url TEXT,
    instructor TEXT DEFAULT 'Jesus Zamora Thowinsson'
);

-- Tabla de Módulos
CREATE TABLE IF NOT EXISTS modules (
    module_id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    title TEXT NOT NULL,
    module_order INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

-- Tabla de Lecciones (Tu DB 📖 Módulos y Lecciones)
CREATE TABLE IF NOT EXISTS lessons (
    lesson_id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content_type TEXT, -- 'video', 'lectura', 'practica'
    content_data TEXT, -- URL de video, o contenido Markdown
    lesson_order INTEGER,
    FOREIGN KEY (module_id) REFERENCES modules (module_id)
);

-- Tabla de Usuarios (para login y progreso)
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, -- En un sistema real, NUNCA guardar contraseñas en texto plano
    full_name TEXT
);

-- Tabla de Progreso (Trackeo de Checkbox)
CREATE TABLE IF NOT EXISTS progress (
    user_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    PRIMARY KEY (user_id, lesson_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id)
);

-- Tabla de Calendario (Tu DB 🗓️ Calendario Unificado)
CREATE TABLE IF NOT EXISTS calendar_events (
    event_id TEXT PRIMARY KEY,
    course_id TEXT, -- Puede ser nulo para eventos generales
    title TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_type TEXT, -- 'Clase en Vivo', 'Fecha Límite', 'Tutoría'
    FOREIGN KEY (course_id) REFERENCES courses (course_id)
);

-- (Podríamos seguir con Evaluaciones, Recursos, etc., siguiendo la misma lógica)

5. **Flujo de Usuario (User Flow) en Streamlit**

1. **Ingreso** (1_🏛️_Campus_Digital.py):
    - Usuario abre la app. st.session_state['logged_in'] es `False`.
    - Se muestra `st.form` de login.
    - Usuario ingresa credenciales. Se llama a `utils.check_login(user, pass)`.
    - Si es exitoso, `st.session_state['logged_in'] = True` y `st.session_state['user_id'] = 'user_id_from_db'`. La página se re-ejecuta.
2. **Campus (Re-ejecución de** `1_🏛️_Campus_Digital.py)`:
    - `st.session_state['logged_in']` es `True`. Se oculta el login.
    - Se muestra el "Catálogo de Cursos" (Vista de Galería). `utils.get_user_courses()` trae los cursos.
    - Los cursos se muestran usando `st.columns` para crear "tarjetas".
    - **Acción**: Usuario hace clic en el botón "Ir al Curso" de "Análisis de Datos".- **Callback**: Se ejecuta `def select_course(id):
        - `st.session_state`['current_course_id']` = 'id_del_curso'
        - `st.switch_page("pages/2_📚_Mis_Cursos.py")`
3. **Aula Virtual** (`pages/2_📚_Mis_Cursos.py`):
    - La página carga. Chequea `if 'current_course_id' in st.session_state:`.
    - Llama a `utils.get_course_details(st.session_state['current_course_id']`).
    - Llama a `utils.get_course_modules_and_lessons(...)`.
    - Renderiza la "Plantilla":
        - `st.title(course['title'])`, `st.image(course['image_url'])`.
        - Se crean un `st.tabs(["Contenido", "Proyectos", "Recursos"])`.
        - Dentro de "Contenido", se itera sobre los módulos: `for module in modules`:. 
        - Se crea un `st.expander(module['title'])` para cada módulo.
        - Dentro del expander, se itera sobre las lecciones: `for lesson in lessons`:.
        - Se muestra `st.checkbox(lesson['title']`, `value=lesson['completed'])`.
        - Si el usuario hace clic en el checkbox, un callback actualiza la DB `(utils.toggle_progress(...))`.
4. **Navegación**: El usuario usa la barra lateral de Streamlit para ir a `pages/3_🗓️_Calendario.py`, que simplemente llama a `utils.get_calendar_events()` y los muestra.