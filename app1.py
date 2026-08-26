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
    st.header("Cargar el dataset")
    uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"]
try:
    if uploaded_file.name.endswith(".csv"):
                # Intentar leer con ';' (muy común en BankMarketing) o con ','
                try:
                    df = pd.read_csv(uploaded_file, sep=";")
                    if df.shape[1] <= 1:  # Si no detectó bien las columnas
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, sep=",")
                except Exception:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)

            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
st.success("¡Archivo cargado correctamente!")

            # 3. Mostrar vista previa del dataset (head)
            st.subheader("Vista previa del dataset (head):")
            st.dataframe(df.head())

            # 4. Mostrar dimensiones del dataset (filas y columnas)
            filas, columnas = df.shape
            st.subheader("Dimensiones del dataset:")
            st.write(f"• **Filas:** {filas:,}")
            st.write(f"• **Columnas:** {columnas}")

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")