import streamlit as st
st.set_page_config(page_title="Repositorio - UNACH", page_icon="Files/Logo.svg", layout="centered")

def menu_principal():
    placeholder = st.empty()  # Crear el contenedor vacío

    # Usar container() para definir las columnas dentro del placeholder
    with placeholder.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # Crear columnas
        with col2:
            st.image("Files/Logo.svg", use_container_width=True)  # Mostrar la imagen en la columna central
    searchbarholder=st.empty()
    with searchbarholder.container():
        st.markdown("<br>",unsafe_allow_html=True)
        st.text_input("Buscar")
    buttonHolder=st.empty()
    with buttonHolder.container():
        col1,col2,col3 =st.columns([1,0.5,1])
        with col2:
            st.markdown("<br><br>",unsafe_allow_html=True)
            if st.button("Todo", use_container_width=True, help="Ver la base de datos completa", ):
                st.switch_page("pages/PIndexado.py")
menu_principal()