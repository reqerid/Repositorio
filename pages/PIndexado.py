import streamlit as st
from PIL import Image
from modules.data_loader import cargar_datos
from modules.utils import mostrar_recurso
from modules.utils import Ayuda as Ayuda

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
        margin-bottom: 0px;
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
            st.markdown(f"""
                <img src="app/static/Logo2.png" alt="Logo" style="display: block; margin-left: auto; margin-right: auto; width: 100%;">
            """, unsafe_allow_html=True)    
        with col1:
            if st.button("⬅ Home", use_container_width=False):
                st.switch_page("pages/Navegación.py")

def mostrar_controles_filtros(data):
    """
    Muestra los filtros en una misma fila y los archivos paginados (6 por página).
    Los filtros de Autor, Año y Extensión están deshabilitados hasta que se selecciona una materia distinta de 'Todas'.
    Incluye botones de 'Anteriores' y 'Siguientes' para navegar y un contador de paginación.
    """
    # Inicializar variables de sesión para ocultar mensajes de ayuda y la página actual
    if "hide_materia_help" not in st.session_state:
        st.session_state.hide_materia_help = False
    if "hide_search_help" not in st.session_state:
        st.session_state.hide_search_help = False
    if 'pagina_actual' not in st.session_state: 
        st.session_state.pagina_actual = 1
    
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
            st.write("-----")
            # Mostrar la fila de filtros en 4 columnas
            cols = st.columns(4)
            # Filtro 1: Materia (obligatorio)
            materias = sorted(set(item["Materia"] for item in data))
            materias.insert(0, "Todas")
            filtro_materia = cols[0].selectbox("Materia", materias)
            
            # Si se mantiene "Todas", los demás filtros se fijan a "Todos" y se deshabilitan.
            if filtro_materia == "Todas":
                filtro_autor = cols[1].selectbox("Autor", ["Todos"], disabled=True)
                filtro_año = cols[2].selectbox("Año", ["Todos"], disabled=True)
                filtro_extension = cols[3].selectbox("Extensión", ["Todos"], disabled=True)
                data_filtrada = data
                # Mostrar mensaje de ayuda para elegir materia (si no se ha ocultado)
                if not st.session_state.hide_materia_help:
                #     msg_col,col_mid, close_col = st.columns([0.5,1,0.5 ])
                #     # with msg_col:
                #     #     st.markdown('<div class="help-message">Estos son los filtros. Primero tienes que elegir la etiqueta materia para que las demás etiquetas se activen.</div>', unsafe_allow_html=True)
                #     with col_mid:
                    if st.button("Estos son los filtros, primero elige tu materia. ✕ ", key="hide_materia_help_button", use_container_width=True):
                        st.session_state.hide_materia_help = True
                        st.rerun()
                st.markdown(Ayuda, unsafe_allow_html=True) #el css de los botones

            else:
                # Si se selecciona una materia específica, se filtra la data y se habilitan los filtros
                data_materia = [item for item in data if item["Materia"] == filtro_materia]
                # Filtro 2: Autor basado en la materia seleccionada.
                autores_unicos = sorted(set(item["Autor"] for item in data_materia))
                opciones_autor = ["Todos"] + autores_unicos if autores_unicos else ["Todos"]
                filtro_autor = cols[1].selectbox("Autor", opciones_autor, disabled=False)
                data_materia_autor = [item for item in data_materia if item["Autor"] == filtro_autor] if filtro_autor != "Todos" else data_materia
                
                # Filtro 3: Año basado en los datos filtrados por Materia y Autor.
                años_unicos = sorted(set(item["Año"] for item in data_materia_autor), reverse=True)
                opciones_año = ["Todos"] + [str(a) for a in años_unicos] if años_unicos else ["Todos"]
                filtro_año = cols[2].selectbox("Año", opciones_año, disabled=False)
                data_materia_autor_año = [item for item in data_materia_autor if str(item["Año"]) == filtro_año] if filtro_año != "Todos" else data_materia_autor
                
                # Filtro 4: Extensión basado en los datos filtrados hasta el momento.
                extensiones_unicas = sorted(set(item["Extensión"] for item in data_materia_autor_año))
                opciones_extension = ["Todos"] + extensiones_unicas if extensiones_unicas else ["Todos"]
                filtro_extension = cols[3].selectbox("Extensión", opciones_extension, disabled=False)
                
                data_filtrada = [
                    item for item in data
                    if (item["Materia"] == filtro_materia)
                    and (filtro_autor == "Todos" or item["Autor"] == filtro_autor)
                    and (filtro_año == "Todos" or str(item["Año"]) == filtro_año)
                    and (filtro_extension == "Todos" or item["Extensión"] == filtro_extension)
                ]
            

            
            query = st.text_input("", "", placeholder="Buscar por título...", key="search_bar", label_visibility="collapsed")
            
            # Aplicar búsqueda si hay texto
            if query.strip():
                data_filtrada = [item for item in data_filtrada if query.lower() in item["Titulo"].lower()]
            # Barra de búsqueda
            if not st.session_state.hide_search_help:
                if st.button("Busca tu recurso ingresando el titulo. ✕ ", key="hide_search_help_button", use_container_width=True):
                    st.session_state.hide_search_help = True
                    st.rerun()

            # Paginación: Mostrar solo 6 archivos por página
            archivos_por_pagina = 6
            total_paginas = (len(data_filtrada) + archivos_por_pagina - 1) // archivos_por_pagina
            
            # Asegurarse de que la página actual no exceda el total de páginas
            if total_paginas > 0 and st.session_state.pagina_actual > total_paginas:
                st.session_state.pagina_actual = total_paginas
            elif total_paginas == 0:
                st.session_state.pagina_actual = 1
            
            # Obtener los archivos de la página actual
            inicio = (st.session_state.pagina_actual - 1) * archivos_por_pagina
            fin = inicio + archivos_por_pagina
            archivos_pagina = data_filtrada[inicio:fin]
            
            # Mostrar los recursos paginados
            if archivos_pagina:
                for i in range(0, len(archivos_pagina), 2):
                    c1, c2, c3, c4 = st.columns(4)
                    # Primer recurso
                    if i < len(archivos_pagina):
                        recurso1 = archivos_pagina[i]
                        with c1:
                            mostrar_recurso(recurso1)
                        with c2:
                            if recurso1["Extensión"].lower() == "pdf":
                                st.markdown(
                                    f"""
                                    <a href="app/static/Libros/{recurso1['Titulo']}.pdf" target="_blank">
                                        <button style="background-color: #007bff; color: white; padding: 10px 20px; 
                                        border: none; border-radius: 5px; cursor: pointer;">
                                            Abrir
                                        </button>
                                    </a>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            st.write(recurso1["Titulo"])
                            st.write(f"**Autor:** {recurso1['Autor']}")
                            st.write(f"**Año:** {recurso1['Año']}")
                            st.write(f"**Extensión:** {recurso1['Extensión']}")
                            st.write("-------")
                    # Segundo recurso
                    if i + 1 < len(archivos_pagina):
                        recurso2 = archivos_pagina[i + 1]
                        with c3:
                            mostrar_recurso(recurso2)
                        with c4:
                            if recurso2["Extensión"].lower() == "pdf":
                                st.markdown(
                                    f"""
                                    <a href="app/static/Libros/{recurso2['Titulo']}.pdf" target="_blank">
                                        <button style="background-color: #007bff; color: white; padding: 10px 20px; 
                                        border: none; border-radius: 5px; cursor: pointer;">
                                            Abrir
                                        </button>
                                    </a>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            st.write(recurso2["Titulo"])
                            st.write(f"**Autor:** {recurso2['Autor']}")
                            st.write(f"**Año:** {recurso2['Año']}")
                            st.write(f"**Extensión:** {recurso2['Extensión']}")
                            st.write("-------")

            else:
                st.warning("No hay archivos disponibles con la combinación de filtros y búsqueda seleccionada.")
            
            # Mostrar contador de paginación
            if total_paginas > 0:
                st.write(f"Página {st.session_state.pagina_actual} de {total_paginas}")
            else:
                st.write("No hay páginas disponibles.")
            
            # Botones de navegación con disabled
            col_anteriores, col_siguientes, col_rell = st.columns([1,1,6])
            with col_anteriores:
                st.button("Anteriores", disabled=(st.session_state.pagina_actual == 1), on_click=lambda: st.session_state.update(pagina_actual=st.session_state.pagina_actual - 1))
            with col_siguientes:
                st.button("Siguientes", disabled=(st.session_state.pagina_actual == total_paginas), on_click=lambda: st.session_state.update(pagina_actual=st.session_state.pagina_actual + 1))
            
            return filtro_materia, filtro_autor, filtro_año, filtro_extension, query

def principal():
    data = cargar_datos("Data/Archivos.json")
    mostrar_encabezado()
    with st.container():
        mostrar_controles_filtros(data)

if __name__ == "__main__":
    principal()