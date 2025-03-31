import streamlit as st
from PIL import Image
import json
import fitz # PyMuPDF
st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="wide")


def principal ():
    # Load data from JSON file
    with open("Data/Archivos.json", "r") as file:
        data = json.load(file)
    
        
    # CSS personalizado para eliminar el padding de los contenedores

    justabutton=st.empty()
    with justabutton.container():
        col1,col2,col3=st.columns([0.2,1,0.2])
        with col2:
            st.markdown("""
                <style>
                @keyframes cambioColores {
                    0% { color: #a4d6f3; }  /* Celeste claro */
                    25% { color: #90cbee; } /* Azul más oscuro */
                    50% { color: #d4af37; } /* Dorado oscuro */
                    75% { color: #78c0e9; } /* Azul suave */
                    100% { color: #a4d6f3; } /* Vuelve al celeste claro */
                }
                .titulo {
                    text-align: center;
                    font-size: 55px; /* Título más grande */
                    font-weight: bold; /* Texto más destacado */
                    animation: cambioColores 4s infinite; /* Animación constante */
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5); /* Sombra ligera */
                }
                </style>
                <h1 class="titulo">REPOSITORIO</h1>
            """, unsafe_allow_html=True)

        with col3:
            st.image("Files/Logo.svg", use_container_width=True)
        with col1:
            if st.button("⬅ Home", use_container_width=False):
                st.switch_page("pages/Navegación.py")
        
    contenedorprincipal = st.empty()
    with contenedorprincipal.container():

            queryDeBusqueda = st.text_input(
                "",
                "",
                placeholder="Título...",
                key="search_bar",
                label_visibility="collapsed"
            )
    
    filtros= st.empty()
    #logica dinámica para filtros.
    AutoresUnicos=list(set(item["Autor"] for item in data))
    AutoresUnicos.sort()
    AutoresUnicos.insert(0,"Todos")

    MateriasUnicas=list(set(item["Materia"] for item in data))
    MateriasUnicas.sort()
    MateriasUnicas.insert(0,"Todas")

    AñosUnicos=list(set(item["Año"] for item in data))
    AñosUnicos.sort(reverse=True)
    AñosUnicos.insert(0,"Todos")

    ExtensionesUnicas=list(set(item["Extensión"] for item in data))
    ExtensionesUnicas.sort()
    ExtensionesUnicas.insert(0,"Todos")

    with filtros.container():
        col0,col1=st.columns([0.3,1])
        with col0:
            st.subheader("Novedades y Páginas oficiales", anchor="novedades")
            Imagenes = ["Files/Logo.png", "Files/Calendario.jpg", "Files/Eventos.jpg"]
            indice = st.slider("", 0, len(Imagenes) - 1)
            imagen = Image.open(Imagenes[indice])
            st.image(imagen, caption="", use_container_width=False, width=300)
        with col1:
            col1,col2,col3,col4=st.columns([1,1,1,1])
            with col1:
                FiltroAutor=st.selectbox("Autor",AutoresUnicos)
            with col2:
                FiltroMateria=st.selectbox("Materia",MateriasUnicas)
            with col3:
                FiltroAño=st.selectbox("Año",AñosUnicos)
            with col4:
                FiltroExtensión=st.selectbox("Extensión",ExtensionesUnicas)

            def renderizar_caratula(ruta_pdf):
                """Render the cover image of a PDF."""
                try:
                    doc = fitz.open(ruta_pdf)
                    primera_pagina = doc[0]
                    pix = primera_pagina.get_pixmap(dpi=150)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    return img
                except Exception as e:
                    st.write("No se pudo cargar la carátula:", e)
                    return None
            
            DatosFiltrados=[
                item for item in data
                if(FiltroAutor=="Todos" or item["Autor"]==FiltroAutor)
                and (FiltroMateria=="Todas" or item["Materia"]==FiltroMateria)
                and (FiltroAño=="Todos" or item["Año"]==FiltroAño)
                and (FiltroExtensión=="Todos" or item["Extensión"]==FiltroExtensión)
            ]

            #logica para la barra de busqueda
            if queryDeBusqueda.strip():
                DatosFiltrados = [
                    item for item in DatosFiltrados
                    if queryDeBusqueda.lower() in item["Titulo"].lower()
                ]
            else:
                DatosFiltrados = [
                    item for item in data
                    if(FiltroAutor=="Todos" or item["Autor"]==FiltroAutor)
                    and (FiltroMateria=="Todas" or item["Materia"]==FiltroMateria)
                    and (FiltroAño=="Todos" or item["Año"]==FiltroAño)
                    and (FiltroExtensión=="Todos" or item["Extensión"]==FiltroExtensión)]
            
            contenedores = {}
            for i in range(0, len(DatosFiltrados), 2):  # Iterar cada dos recursos para generar filas
                # Crear una fila con cuatro columnas
                col1, col2, col3, col4 = st.columns(4)

                # Primer recurso (si está disponible)
                if i < len(DatosFiltrados):
                    recurso1 = DatosFiltrados[i]
                    with col1:  # Portada del primer recurso
                        if recurso1["Extensión"].lower() == "pdf":
                            ruta_pdf1 = f"static/Libros/{recurso1['Titulo']}.pdf"
                            caratula1 = renderizar_caratula(ruta_pdf1)
                            if caratula1:
                                st.image(caratula1, caption="Carátula", use_container_width=True)

                    with col2:  # Información del primer recurso
                        st.write(recurso1["Titulo"])
                        st.write(f"**Autor:** {recurso1['Autor']}")
                        st.write(f"**Materia:** {recurso1['Materia']}")
                        st.write(f"**Año:** {recurso1['Año']}")
                        st.write(f"**Extensión:** {recurso1['Extensión']}")
                        if recurso1["Extensión"].lower() == "pdf":
                            st.markdown(
                                f"""
                                <a href="app/static/Libros/{recurso1['Titulo']}.pdf" target="_blank">
                                    <button style="background-color: #007bff; color: white; padding: 10px 20px; 
                                    border: none; border-radius: 5px; cursor: pointer;">
                                        Abrir {recurso1['Titulo']}
                                    </button>
                                </a>
                                """,
                                unsafe_allow_html=True,
                            )

                # Segundo recurso (si está disponible)
                if i + 1 < len(DatosFiltrados):
                    recurso2 = DatosFiltrados[i + 1]
                    with col3:  # Portada del segundo recurso
                        if recurso2["Extensión"].lower() == "pdf":
                            ruta_pdf2 = f"static/Libros/{recurso2['Titulo']}.pdf"
                            caratula2 = renderizar_caratula(ruta_pdf2)
                            if caratula2:
                                st.image(caratula2, caption="Carátula", use_container_width=True)

                    with col4:  # Información del segundo recurso
                        st.write(recurso2["Titulo"])
                        st.write(f"**Autor:** {recurso2['Autor']}")
                        st.write(f"**Materia:** {recurso2['Materia']}")
                        st.write(f"**Año:** {recurso2['Año']}")
                        st.write(f"**Extensión:** {recurso2['Extensión']}")
                        if recurso2["Extensión"].lower() == "pdf":
                            st.markdown(
                                f"""
                                <a href="app/static/Libros/{recurso2['Titulo']}.pdf" target="_blank">
                                    <button style="background-color: #007bff; color: white; padding: 10px 20px; 
                                    border: none; border-radius: 5px; cursor: pointer;">
                                        Abrir {recurso2['Titulo']}
                                    </button>
                                </a>
                                """,
                                unsafe_allow_html=True
                            )

        
#---------------------------------------------------------------



principal()