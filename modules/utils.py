# modules/utils.py
import fitz
from PIL import Image
import streamlit as st


#estilos para el botón de ayuda#
Ayuda ="""
    <style>
    div.stButton > button {
        background-color: #F7F7F7; /* Gris claro para minimalismo */
        color: #2D3748; /* Gris azulado oscuro para contraste */
        border: none; /* Sin bordes para look limpio */
        border-radius: 8px; /* Bordes ligeramente redondeados */
        padding: 8px 16px; /* Padding compacto */
        font-size: 14px; /* Fuente pequeña y elegante */
        font-weight: 400; /* Peso ligero */
        font-family: 'Arial', sans-serif; /* Fuente moderna */
        box-shadow: 0 0 10px rgba(226, 232, 240, 0.5); /* Sombra inicial */
        animation: pulse 2s infinite ease-in-out; /* Animación en bucle */
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #E2E8F0; /* Gris más claro al hover */
        transform: scale(1.05); /* Ligeramente más grande */
    }
    @keyframes pulse {
        0% {
            box-shadow: 0 0 10px rgba(226, 232, 240, 0.5);
        }
        50% {
            box-shadow: 0 0 20px rgba(226, 232, 240, 0.8);
        }
        100% {
            box-shadow: 0 0 10px rgba(226, 232, 240, 0.5);
        }
    }
    </style>
    """

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
