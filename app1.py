import streamlit as st
import pandas as pd
st.title("PROYECTO - BankMarketing")
st.sidebar.title("Menú de navegación")
Opciones = ["Inicio", "Carga del dataset"]
Seleccion = st.sidebar.radio("Seleccione una opción", Opciones)
if Seleccion == "Inicio":
    st.write("El objetivo del proyecto esanalizar los datos de la última campaña de una entidad financiera para descubrir relaciones y comportamientos relevantes entre las variables")
    st.write("Alumno: Mario Alberto Ormeño Bobadilla")
    st.write("Especialización en Python for Analytics")
    st.write("2026")
    st.write("DATASET: Institución financiera que busca entender los factores que influyen en la aceptación de sus campañas de marketing. Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12% a 8%, afectando los bonos de los ejecutivos comerciales.")
elif Seleccion == "Carga del dataset":
    st.write("Cargar el dataset")
    uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa del dataset:")
        st.dataframe(df.head())