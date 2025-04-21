# modules/utils.py
import fitz
from PIL import Image
import streamlit as st

def renderizar_caratula(ruta_pdf):
    """
    Renderiza la portada de un PDF.
    """
    try:
        doc = fitz.open(ruta_pdf)
        primera_pagina = doc[0]
        pix = primera_pagina.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    except Exception as e:
        st.write(f"No se pudo cargar la carátula: {e}")
        return None

def mostrar_recurso(recurso):
    """
    Muestra el recurso basándose en el valor de "Extensión".
    Soporta PDF, MP4 (video) y MP3 (audio).
    """
    ext = recurso["Extensión"].strip().lower()
    if ext == "pdf":
        ruta_pdf = f"static/Libros/{recurso['Titulo']}.pdf"
        caratula = renderizar_caratula(ruta_pdf)
        if caratula:
            st.image(caratula, caption="Carátula", use_container_width=True)
    elif ext == "mp4":
        ruta_video = f"static/Videos/{recurso['Titulo']}.mp4"
        try:
            st.video(ruta_video)
        except Exception:
            try:
                st.video(recurso.get("Url", ""))
            except Exception as e:
                st.write(f"Error al cargar el video: {e}")
    elif ext == "mp3":
        ruta_audio = f"static/Audios/{recurso['Titulo']}.mp3"
        try:
            st.audio(ruta_audio)
        except Exception as e:
            st.write(f"Error al cargar el audio: {e}")
