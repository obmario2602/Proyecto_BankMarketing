import streamlit as st
st.title("PROYECTO - BankMarketing")
st.sidebar.title("Menú de navegación")
Opciones = ["Inicio", "Carga del dataset"]
Seleccion = st.sidebar.radio("Seleccione una opción", Opciones)
if Opciones == "Inicio":
    st.write("El objetivo del proyecto esanalizar los datos de la última campaña de una entidad financiera para descubrir relaciones y comportamientos relevantes entre las variables")
    st.write("Alumno: Mario Alberto Ormeño Bobadilla")
    st.write("Especialización en Python for Analytics")
    st.write("2026")
    