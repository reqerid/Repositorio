import streamlit as st
import json
from PIL import Image
import fitz  # PyMuPDF
st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="centered")

def menu_principal():

        # Leer el archivo JSON
    with open("Data/Archivos.json", "r") as file:
        data = json.load(file)
    DatosFiltrados= data

    #funcion para renderizar la caratula
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

    placeholder = st.empty()  # Crear el contenedor vacío

    # Usar container() para definir las columnas dentro del placeholder
    with placeholder.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # Crear columnas
        with col2:
            st.image("Files/Logo.svg", use_container_width=True)  # Mostrar la imagen en la columna central

    searchbarholder=st.empty()
    with searchbarholder.container():
        st.markdown("<br>",unsafe_allow_html=True)
        queryDeBusqueda = st.text_input(
            "",
            "",
            placeholder="Título...",
            key="search_bar",
            label_visibility="collapsed"
        )
        if queryDeBusqueda.strip():
            DatosFiltrados = [
                item for item in DatosFiltrados
                if queryDeBusqueda.lower() in item["Titulo"].lower()
            ]
            
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
                            elif recurso1["Extensión"].strip().lower() == "mp4":
                                ruta_video1 = f"static/Videos/{recurso1['Titulo']}.mp4"
                                try:
                                    # Intenta reproducir el video desde la ruta generada
                                    st.video(ruta_video1)
                                except Exception as e:
                                    # Si ocurre un error, intenta reproducirlo con otra fuente
                                    try:
                                        st.video(recurso1["Url"])
                                    except Exception as fallback_error:
                                        st.write(f"No se pudo cargar el video alternativo. Error: {fallback_error}")
                            elif recurso1["Extensión"].strip().lower()=="mp3":
                                ruta_audio1=f"static/Audios/{recurso1['Titulo']}.mp3"
                                try:
                                    st.audio(ruta_audio1)
                                except Exception as e:
                                    #si ocurre un error enviamos un mensaje de error
                                    st.write(f"No se pudo cargar el audio alternativo. Error: {e}")


                        with col2:  # Información del primer recurso
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
                            st.write(f"**Materia:** {recurso1['Materia']}")
                            st.write(f"**Año:** {recurso1['Año']}")
                            st.write(f"**Extensión:** {recurso1['Extensión']}")
                            st.write(" ")


                    # Segundo recurso (si está disponible)
                    if i + 1 < len(DatosFiltrados):
                        recurso2 = DatosFiltrados[i + 1]
                        with col3:  # Portada del segundo recurso
                            if recurso2["Extensión"].lower() == "pdf":
                                ruta_pdf2 = f"static/Libros/{recurso2['Titulo']}.pdf"
                                caratula2 = renderizar_caratula(ruta_pdf2)
                                if caratula2:
                                    st.image(caratula2, caption="Carátula", use_container_width=True)
                            elif recurso2["Extensión"].strip().lower() == "mp4":
                                ruta_video1 = f"static/Videos/{recurso2['Titulo']}.mp4"
                                try:
                                    # Intenta reproducir el video desde la ruta generada
                                    st.video(ruta_video1)
                                except Exception as e:
                                    # Si ocurre un error, intenta reproducirlo con otra fuente
                                    try:
                                        st.video(recurso2["Url"])
                                    except Exception as fallback_error:
                                        st.write(f"No se pudo cargar el video alternativo. Error: {fallback_error}")
                            elif recurso2["Extensión"].strip().lower()=="mp3":
                                ruta_audio2=f"static/Audios/{recurso2['Titulo']}.mp3"
                                try:
                                    st.audio(ruta_audio2)
                                except Exception as e:
                                    #si ocurre un error enviamos un mensaje de error
                                    st.write(f"No se pudo cargar el audio alternativo. Error: {e}")



                        with col4:  # Información del segundo recurso
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
                                    unsafe_allow_html=True
                                )
                            st.write(recurso2["Titulo"])
                            st.write(f"**Autor:** {recurso2['Autor']}")
                            st.write(f"**Materia:** {recurso2['Materia']}")
                            st.write(f"**Año:** {recurso2['Año']}")
                            st.write(f"**Extensión:** {recurso2['Extensión']}")
                            st.write(" ")


    buttonHolder=st.empty()
    with buttonHolder.container():
        col1,col2,col3 =st.columns([1,0.5,1])
        with col2:
            st.markdown("<br><br>",unsafe_allow_html=True)
            if st.button("Todo", use_container_width=True, help="Ver la base de datos completa", ):
                st.switch_page("pages/PIndexado.py")
menu_principal()