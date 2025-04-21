import streamlit as st
from PIL import Image
from modules.data_loader import cargar_datos
from modules.utils import renderizar_caratula, mostrar_recurso

st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="wide")

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

def obtener_filtros(data):
    autores = list(set(item["Autor"] for item in data))
    autores.sort()
    autores.insert(0, "Todos")
    
    materias = list(set(item["Materia"] for item in data))
    materias.sort()
    materias.insert(0, "Todas")
    
    años = list(set(item["Año"] for item in data))
    años.sort(reverse=True)
    años.insert(0, "Todos")
    
    extensiones = list(set(item["Extensión"] for item in data))
    extensiones.sort()
    extensiones.insert(0, "Todos")
    
    return autores, materias, años, extensiones

def mostrar_controles_filtros(data):
    # Contenedor que separa la columna izquierda de la derecha
    with st.container():
        col0, col1 = st.columns([0.3, 1])
        
        # Columna izquierda: sección de novedades
        with col0:
            st.subheader("Novedades y Páginas oficiales", anchor="novedades")
            imagenes = ["Files/Logo.png", "Files/Calendario.jpg", "Files/Eventos.jpg"]
            indice = st.slider("Selecciona imagen", 0, len(imagenes)-1, 2)
            imagen = Image.open(imagenes[indice])
            st.image(imagen, caption="", use_container_width=False, width=300)
        
        # Columna derecha: Filtros, barra de búsqueda y recursos
        with col1:
            # Obtener valores únicos para los filtros
            autores, materias, años, extensiones = obtener_filtros(data)
            col1_box, col2_box, col3_box, col4_box = st.columns(4)
            filtro_autor = col1_box.selectbox("Autor", autores)
            filtro_materia = col2_box.selectbox("Materia", materias)
            filtro_año = col3_box.selectbox("Año", años)
            filtro_extension = col4_box.selectbox("Extensión", extensiones)
    
            # Barra de búsqueda (query)
            query = st.text_input("", "", placeholder="Título...", key="search_bar", label_visibility="collapsed")
            
            # Filtrar los datos usando los filtros y el query
            datos_filtrados = [
                item for item in data 
                if (filtro_autor == "Todos" or item["Autor"] == filtro_autor)
                   and (filtro_materia == "Todas" or item["Materia"] == filtro_materia)
                   and (filtro_año == "Todos" or item["Año"] == filtro_año)
                   and (filtro_extension == "Todos" or item["Extensión"] == filtro_extension)
            ]
            if query.strip():
                datos_filtrados = [item for item in datos_filtrados if query.lower() in item["Titulo"].lower()]
            
            # Mostrar los recursos justo debajo del query en la misma columna
            for i in range(0, len(datos_filtrados), 2):
                col1_res, col2_res, col3_res, col4_res = st.columns(4)
                
                # Primer recurso
                if i < len(datos_filtrados):
                    recurso1 = datos_filtrados[i]
                    with col1_res:
                        mostrar_recurso(recurso1)
                    with col2_res:
                        if recurso1["Extensión"].strip().lower() == "pdf":
                            st.markdown(
                                f"""
                                <a href="app/static/Libros/{recurso1['Titulo']}.pdf" target="_blank">
                                    <button style="background-color: #007bff; 
                                                    color: white; 
                                                    padding: 10px 20px; 
                                                    border: none; 
                                                    border-radius: 5px; 
                                                    cursor: pointer;">Abrir</button>
                                </a>
                                """, unsafe_allow_html=True)
                        st.write(recurso1["Titulo"])
                        st.write(f"**Autor:** {recurso1['Autor']}")
                        st.write(f"**Materia:** {recurso1['Materia']}")
                        st.write(f"**Año:** {recurso1['Año']}")
                        st.write(f"**Extensión:** {recurso1['Extensión']}")
                        st.write(" ")
                # Segundo recurso
                if i + 1 < len(datos_filtrados):
                    recurso2 = datos_filtrados[i + 1]
                    with col3_res:
                        mostrar_recurso(recurso2)
                    with col4_res:
                        if recurso2["Extensión"].strip().lower() == "pdf":
                            st.markdown(
                                f"""
                                <a href="app/static/Libros/{recurso2['Titulo']}.pdf" target="_blank">
                                    <button style="background-color: #007bff; 
                                                    color: white; 
                                                    padding: 10px 20px; 
                                                    border: none; 
                                                    border-radius: 5px; 
                                                    cursor: pointer;">Abrir</button>
                                </a>
                                """, unsafe_allow_html=True)
                        st.write(recurso2["Titulo"])
                        st.write(f"**Autor:** {recurso2['Autor']}")
                        st.write(f"**Materia:** {recurso2['Materia']}")
                        st.write(f"**Año:** {recurso2['Año']}")
                        st.write(f"**Extensión:** {recurso2['Extensión']}")
                        st.write(" ")
                        
            return filtro_autor, filtro_materia, filtro_año, filtro_extension, query

def aplicar_filtros(data, filtro_autor, filtro_materia, filtro_año, filtro_extension, query):
    datos_filtrados = [
        item for item in data
        if (filtro_autor == "Todos" or item["Autor"] == filtro_autor)
           and (filtro_materia == "Todas" or item["Materia"] == filtro_materia)
           and (filtro_año == "Todos" or item["Año"] == filtro_año)
           and (filtro_extension == "Todos" or item["Extensión"] == filtro_extension)
    ]
    if query.strip():
        datos_filtrados = [item for item in datos_filtrados if query.lower() in item["Titulo"].lower()]
    return datos_filtrados

def mostrar_recursos(datos):
    # Si por alguna razón se desea usar esta función fuera de mostrar_controles_filtros
    for i in range(0, len(datos), 2):
        col1, col2, col3, col4 = st.columns(4)
        if i < len(datos):
            recurso1 = datos[i]
            with col1:
                mostrar_recurso(recurso1)
            with col2:
                if recurso1["Extensión"].strip().lower() == "pdf":
                    st.markdown(
                        f"""
                        <a href="app/static/Libros/{recurso1['Titulo']}.pdf" target="_blank">
                            <button style="background-color: #007bff; 
                                            color: white; 
                                            padding: 10px 20px; 
                                            border: none; 
                                            border-radius: 5px; 
                                            cursor: pointer;">Abrir</button>
                        </a>
                        """, unsafe_allow_html=True)
                st.write(recurso1["Titulo"])
                st.write(f"**Autor:** {recurso1['Autor']}")
                st.write(f"**Materia:** {recurso1['Materia']}")
                st.write(f"**Año:** {recurso1['Año']}")
                st.write(f"**Extensión:** {recurso1['Extensión']}")
                st.write(" ")
        if i + 1 < len(datos):
            recurso2 = datos[i + 1]
            with col3:
                mostrar_recurso(recurso2)
            with col4:
                if recurso2["Extensión"].strip().lower() == "pdf":
                    st.markdown(
                        f"""
                        <a href="app/static/Libros/{recurso2['Titulo']}.pdf" target="_blank">
                            <button style="background-color: #007bff; 
                                            color: white; 
                                            padding: 10px 20px; 
                                            border: none; 
                                            border-radius: 5px; 
                                            cursor: pointer;">Abrir</button>
                        </a>
                        """, unsafe_allow_html=True)
                st.write(recurso2["Titulo"])
                st.write(f"**Autor:** {recurso2['Autor']}")
                st.write(f"**Materia:** {recurso2['Materia']}")
                st.write(f"**Año:** {recurso2['Año']}")
                st.write(f"**Extensión:** {recurso2['Extensión']}")
                st.write(" ")

def principal():
    data = cargar_datos("Data/Archivos.json")
    mostrar_encabezado()
    
    # La idea es que los controles, la barra de búsqueda y la exhibición de recursos se muestren en un mismo contenedor
    with st.container():
        filtro_autor, filtro_materia, filtro_año, filtro_extension, query = mostrar_controles_filtros(data)
        # (Aquí se podría aplicar la función aplicar_filtros si se desea)
        datos_filtrados = aplicar_filtros(data, filtro_autor, filtro_materia, filtro_año, filtro_extension, query)
        # Se puede volver a llamar a mostrar_recursos() aquí, o bien confiar en lo que se renderizó dentro de mostrar_controles_filtros
        # Para mantener la coherencia, si se requiere mostrar recursos en otro contenedor, se puede llamar:
        # mostrar_recursos(datos_filtrados)

if __name__ == "__main__":
    principal()
