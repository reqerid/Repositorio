import streamlit as st
import json
from PIL import Image
import fitz  # PyMuPDF

st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="centered")

# Inyectar CSS global para el icono de lupa y los mensajes de ayuda
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

def menu_principal():
    # Leer el archivo JSON
    with open("Data/Archivos.json", "r") as file:
        data = json.load(file)
    DatosFiltrados = data.copy()

    # Función para renderizar la carátula
    def renderizar_caratula(ruta_pdf):
        """Render the cover image of a PDF."""
        try:
            doc = fitz.open(ruta_pdf)
            primera_pagina = doc[0]
            pix = primera_pagina.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return img
        except Exception as e:
            st.write(f"No se pudo cargar la carátula: {e}")
            return None

    # Mostrar logo centrado
    placeholder = st.empty()
    with placeholder.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image("Files/Logo.svg", use_container_width=True)

    # Inicializar variables de sesión para los mensajes de ayuda
    if "hide_search_help" not in st.session_state:
        st.session_state.hide_search_help = False
    if "hide_button_help" not in st.session_state:
        st.session_state.hide_button_help = False

    # Contenedor para la barra de búsqueda
    searchbarholder = st.empty()
    with searchbarholder.container():
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mensaje de ayuda para la barra de búsqueda
        if not st.session_state.hide_search_help:
            col_msg, col_close = st.columns([0.9, 0.1])
            with col_msg:
                st.markdown(
                    '<div class="help-message">Aquí puedes realizar la búsqueda de tus archivos en el repositorio ingresando el título.</div>',
                    unsafe_allow_html=True
                )
            with col_close:
                if st.button("✕", key="hide_search_help_button", help="Ocultar mensaje"):
                    st.session_state.hide_search_help = True
                    st.rerun()

        # Barra de búsqueda
        queryDeBusqueda = st.text_input(
            "",
            "",
            placeholder="Buscar por título...",
            key="search_bar",
            label_visibility="collapsed"
        )
        
        if queryDeBusqueda.strip():
            DatosFiltrados = [
                item for item in DatosFiltrados
                if queryDeBusqueda.lower() in item["Titulo"].lower()
            ]
            
            if not DatosFiltrados:
                st.error("No se encontró ningún archivo con ese título.")
            else:
                for i in range(0, len(DatosFiltrados), 2):
                    col1, col2, col3, col4 = st.columns(4)

                    # Primer recurso
                    if i < len(DatosFiltrados):
                        recurso1 = DatosFiltrados[i]
                        with col1:
                            if recurso1["Extensión"].lower() == "pdf":
                                ruta_pdf1 = f"static/Libros/{recurso1['Titulo']}.pdf"
                                caratula1 = renderizar_caratula(ruta_pdf1)
                                if caratula1:
                                    st.image(caratula1, caption="Carátula", use_container_width=True)
                            elif recurso1["Extensión"].lower() == "mp4":
                                ruta_video1 = f"static/Videos/{recurso1['Titulo']}.mp4"
                                try:
                                    st.video(ruta_video1)
                                except Exception:
                                    try:
                                        st.video(recurso1["Url"])
                                    except Exception as fallback_error:
                                        st.write(f"No se pudo cargar el video alternativo: {fallback_error}")
                            elif recurso1["Extensión"].lower() == "mp3":
                                ruta_audio1 = f"static/Audios/{recurso1['Titulo']}.mp3"
                                try:
                                    st.audio(ruta_audio1)
                                except Exception as e:
                                    st.write(f"No se pudo cargar el audio alternativo: {e}")
                        with col2:
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
                                    unsafe_allow_html=True
                                )
                            st.write(recurso1["Titulo"])
                            st.write(f"**Autor:** {recurso1['Autor']}")
                            st.write(f"**Materia:** {recurso1['Materia']}")
                            st.write(f"**Año:** {recurso1['Año']}")
                            st.write(f"**Extensión:** {recurso1['Extensión']}")
                            st.write(" ")

                    # Segundo recurso
                    if i + 1 < len(DatosFiltrados):
                        recurso2 = DatosFiltrados[i + 1]
                        with col3:
                            if recurso2["Extensión"].lower() == "pdf":
                                ruta_pdf2 = f"static/Libros/{recurso2['Titulo']}.pdf"
                                caratula2 = renderizar_caratula(ruta_pdf2)
                                if caratula2:
                                    st.image(caratula2, caption="Carátula", use_container_width=True)
                            elif recurso2["Extensión"].lower() == "mp4":
                                ruta_video2 = f"static/Videos/{recurso2['Titulo']}.mp4"
                                try:
                                    st.video(ruta_video2)
                                except Exception:
                                    try:
                                        st.video(recurso2["Url"])
                                    except Exception as fallback_error:
                                        st.write(f"No se pudo cargar el video alternativo: {fallback_error}")
                            elif recurso2["Extensión"].lower() == "mp3":
                                ruta_audio2 = f"static/Audios/{recurso2['Titulo']}.mp3"
                                try:
                                    st.audio(ruta_audio2)
                                except Exception as e:
                                    st.write(f"No se pudo cargar el audio alternativo: {e}")
                        with col4:
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

    # Contenedor para el botón "Todo" y mensaje de ayuda
    buttonHolder = st.empty()
    with buttonHolder.container():
        col1, col2, col3 = st.columns([1, 0.5, 1])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Todo", use_container_width=True, help="Ver la base de datos completa"):
                st.switch_page("pages/PIndexado.py")
        with col3:
            if not st.session_state.hide_button_help:
                col_msg, col_close = st.columns([0.9, 0.1])
                with col_msg:
                    st.markdown(
                        '<div class="help-message">O si lo prefieres, puedes ver todo nuestro repositorio completo dando click.</div>',
                        unsafe_allow_html=True
                    )
                with col_close:
                    if st.button("✕", key="hide_button_help_button", help="Ocultar mensaje"):
                        st.session_state.hide_button_help = True
                        st.rerun()

menu_principal()