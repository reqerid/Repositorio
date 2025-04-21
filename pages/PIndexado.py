import streamlit as st
from PIL import Image
from modules.data_loader import cargar_datos
from modules.utils import mostrar_recurso

st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="wide")


# Inyectar CSS global para el icono de lupa en el input de búsqueda y para los mensajes de ayuda
st.markdown(
    """
    <style>
    input[placeholder="Buscar por título..."] {
        background-image: url("https://cdn-icons-png.flaticon.com/512/622/622669.png");
        background-repeat: no-repeat;
        background-position: 5px center;
        background-size: 20px;
        padding-left: 30px;
    }
    .help-message {
        background-color: rgba(233, 236, 239, 0.85);
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
        color: #333;
        animation: fadeIn 1.5s ease-in-out;
        margin-bottom: 10px;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

def mostrar_encabezado():
    with st.container():
        col1, col2, col3 = st.columns([0.2, 1, 0.2])
        with col2:
            st.markdown(
                """
                <style>
                @keyframes cambioColores {
                    0% { color: #a4d6f3; }
                    25% { color: #90cbee; }
                    50% { color: #d4af37; }
                    75% { color: #78c0e9; }
                    100% { color: #a4d6f3; }
                }
                .titulo {
                    text-align: center;
                    font-size: 55px;
                    font-weight: bold;
                    animation: cambioColores 4s infinite;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                }
                </style>
                <h1 class="titulo">REPOSITORIO</h1>
                """, 
                unsafe_allow_html=True
            )
        with col3:
            st.image("Files/Logo.svg", use_container_width=True)
        with col1:
            if st.button("⬅ Home", use_container_width=False):
                st.switch_page("pages/Navegación.py")

def mostrar_controles_filtros(data):
    """
    Muestra los filtros en una misma fila. El filtro de Materia es obligatorio y, si se mantiene en "Todas",
    se muestra un mensaje de ayuda que indica que primero se debe elegir la materia para activar los demás filtros.
    Además, se incluye una barra de búsqueda intuitiva (con un mensaje de ayuda y un icono en el input).
    """
    # Inicializar variables de sesión para ocultar mensajes de ayuda si el usuario lo decide
    if "hide_materia_help" not in st.session_state:
        st.session_state.hide_materia_help = False
    if "hide_search_help" not in st.session_state:
        st.session_state.hide_search_help = False
    
    with st.container():
        # Dividir la pantalla en dos columnas: Izquierda para novedades y derecha para filtros y búsqueda.
        col0, col1 = st.columns([0.3, 1])
        
        # Columna izquierda: Sección de novedades.
        with col0:
            st.subheader("Novedades y Páginas oficiales", anchor="novedades")
            imagenes = ["Files/Logo.png", "Files/Calendario.jpg", "Files/Eventos.jpg"]
            indice = st.slider("Selecciona imagen", 0, len(imagenes) - 1, 2)
            imagen = Image.open(imagenes[indice])
            st.image(imagen, caption="", use_container_width=False, width=300)
        
        # Columna derecha: Filtros y barra de búsqueda.
        with col1:
            # Mostrar la fila de filtros en 4 columnas.
            cols = st.columns(4)
            # Filtro 1: Materia (obligatorio)
            materias = sorted(set(item["Materia"] for item in data))
            materias.insert(0, "Todas")
            filtro_materia = cols[0].selectbox("Materia", materias)
            
            # Si se mantiene "Todas", los demás filtros se fijan a "Todos" y se muestra un mensaje de ayuda.
            if filtro_materia == "Todas":
                filtro_autor = cols[1].selectbox("Autor", ["Todos"])
                filtro_año = cols[2].selectbox("Año", ["Todos"])
                filtro_extension = cols[3].selectbox("Extensión", ["Todos"])
                data_filtrada = data
                # Mostrar mensaje de ayuda para elegir materia (si no se ha ocultado)
                if not st.session_state.hide_materia_help:
                    msg_col, close_col = st.columns([0.9, 0.1])
                    with msg_col:
                        st.markdown('<div class="help-message">Primero tienes que elegir la etiqueta materia para que las demás etiquetas se activen.</div>', unsafe_allow_html=True)
                    with close_col:
                        if st.button("✕", key="hide_materia_help_button", help="Ocultar mensaje"):
                            st.session_state.hide_materia_help = True
            else:
                # Si se selecciona una materia específica, se filtra la data
                data_materia = [item for item in data if item["Materia"] == filtro_materia]
                # Filtro 2: Autor basado en la materia seleccionada.
                autores_unicos = sorted(set(item["Autor"] for item in data_materia))
                opciones_autor = ["Todos"] + autores_unicos if autores_unicos else ["Todos"]
                filtro_autor = cols[1].selectbox("Autor", opciones_autor)
                data_materia_autor = [item for item in data_materia if item["Autor"] == filtro_autor] if filtro_autor != "Todos" else data_materia
                
                # Filtro 3: Año basado en los datos filtrados por Materia y Autor.
                años_unicos = sorted(set(item["Año"] for item in data_materia_autor), reverse=True)
                opciones_año = ["Todos"] + [str(a) for a in años_unicos] if años_unicos else ["Todos"]
                filtro_año = cols[2].selectbox("Año", opciones_año)
                data_materia_autor_año = [item for item in data_materia_autor if str(item["Año"]) == filtro_año] if filtro_año != "Todos" else data_materia_autor
                
                # Filtro 4: Extensión basado en los datos filtrados hasta el momento.
                extensiones_unicas = sorted(set(item["Extensión"] for item in data_materia_autor_año))
                opciones_extension = ["Todos"] + extensiones_unicas if extensiones_unicas else ["Todos"]
                filtro_extension = cols[3].selectbox("Extensión", opciones_extension)
                
                data_filtrada = [
                    item for item in data
                    if (item["Materia"] == filtro_materia)
                    and (filtro_autor == "Todos" or item["Autor"] == filtro_autor)
                    and (filtro_año == "Todos" or str(item["Año"]) == filtro_año)
                    and (filtro_extension == "Todos" or item["Extensión"] == filtro_extension)
                ]
            
            # Mostrar mensaje de ayuda para la barra de búsqueda (ocultable) justo antes del input.
            if not st.session_state.hide_search_help:
                msg_col, close_col = st.columns([0.9, 0.1])
                with msg_col:
                    st.markdown('<div class="help-message">Aquí puedes buscar archivos por título.</div>', unsafe_allow_html=True)
                with close_col:
                    if st.button("✕", key="hide_search_help_button", help="Ocultar mensaje"):
                        st.session_state.hide_search_help = True
            
            # Barra de búsqueda (no se agrega un <br> extra para evitar espacios innecesarios)
            query = st.text_input("", "", placeholder="Buscar por título...", key="search_bar", label_visibility="collapsed")
            
            # Si se ingresa texto en la búsqueda, ajustar la data filtrada
            if query.strip():
                data_filtrada = [item for item in data_filtrada if query.lower() in item["Titulo"].lower()]
            
            # Mostrar los recursos filtrados manteniendo la distribución original (filas de 2 recursos en 4 columnas)
            if data_filtrada:
                for i in range(0, len(data_filtrada), 2):
                    c1, c2, c3, c4 = st.columns(4)
                    # Primer recurso
                    if i < len(data_filtrada):
                        recurso1 = data_filtrada[i]
                        with c1:
                            mostrar_recurso(recurso1)
                        with c2:
                            st.write(recurso1["Titulo"])
                            st.write(f"**Autor:** {recurso1['Autor']}")
                            st.write(f"**Año:** {recurso1['Año']}")
                            st.write(f"**Extensión:** {recurso1['Extensión']}")
                    # Segundo recurso
                    if i + 1 < len(data_filtrada):
                        recurso2 = data_filtrada[i + 1]
                        with c3:
                            mostrar_recurso(recurso2)
                        with c4:
                            st.write(recurso2["Titulo"])
                            st.write(f"**Autor:** {recurso2['Autor']}")
                            st.write(f"**Año:** {recurso2['Año']}")
                            st.write(f"**Extensión:** {recurso2['Extensión']}")
            else:
                st.warning("No hay archivos disponibles con la combinación de filtros y búsqueda seleccionada.")
            
            return filtro_materia, filtro_autor, filtro_año, filtro_extension, query

def principal():
    data = cargar_datos("Data/Archivos.json")
    mostrar_encabezado()
    with st.container():
        mostrar_controles_filtros(data)

if __name__ == "__main__":
    principal()
