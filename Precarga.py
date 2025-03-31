import streamlit as st
import time
import base64

# Vistas
# Configuración de la página

st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="centered")

def animacion():
    # Crear un contenedor para la animación
    placeholder = st.empty()

    # Leer y codificar la imagen en base64
    with open("Files/Logo.png", "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode()

    # Usar el contenedor para incrustar HTML y CSS
    placeholder.markdown(f"""
        <style>
            /* Contenedor principal centrado */
            .splash-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 70vh;
            }}
            /* Clase para el logo animado */
            .animated-logo {{
                width: 300px;
                opacity: 0;
                animation: fadeIn 2s ease-in-out forwards;
            }}
            @keyframes fadeIn {{
                0% {{
                    opacity: 0;
                    transform: scale(0.8);
                }}
                50% {{
                    opacity: 0.5;
                    transform: scale(1.05);
                }}
                100% {{
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
        </style>
        <div class="splash-container">
            <img src="data:image/png;base64,{encoded_img}" alt="Logo UNACH" class="animated-logo">
        </div>
    """, unsafe_allow_html=True)

    # Esperar a que termine la animación
    time.sleep(3)

    # Limpiar el placeholder
    placeholder.empty()

# Llamar a la función de animación
animacion()
st.switch_page("pages/Navegación.py")
#PIndexado= st.Page("PIndexado.py", title="Indexado")
#PaginaNavegación = st.Page("Navegación.py", title="Navegación", default=True)
#pg=st.navigation([PaginaNavegación, PIndexado], position="hidden")
#PIndexado.run()