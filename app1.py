import streamlit as st
st.title("PROYECTO - BankMarketing")
st.sidebar.title("Menú de navegación")
Opciones = ["Inicio", "Análisis Exploratorio de Datos", "Modelos de Machine Learning", "Conclusiones"]
Seleccion = st.sidebar.radio("Seleccione una opción", Opciones)