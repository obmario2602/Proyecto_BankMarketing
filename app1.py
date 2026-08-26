import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PROYECTO - BankMarketing", layout="wide"
)  # Opcional: aprovecha mejor el espacio

st.title("PROYECTO - BankMarketing")
st.sidebar.title("Menú de navegación")


# Función personalizada requerida para el Ítem 2
def clasificar_variables(df):
    col_numericas = df.select_dtypes(
        include=["int64", "float64", "int32"]
    ).columns.tolist()
    col_categoricas = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    return {
        "numericas": col_numericas,
        "cant_numericas": len(col_numericas),
        "categoricas": col_categoricas,
        "cant_categoricas": len(col_categoricas),
    }


# Menú Principal
Opciones = ["Inicio", "Carga del dataset", "Análisis Exploratorio (EDA)"]
Seleccion = st.sidebar.radio("Seleccione una opción", Opciones)

# Variable de sesión para conservar los datos entre pestañas
if "df" not in st.session_state:
    st.session_state["df"] = None

# --- OPCIÓN 1: INICIO ---
if Seleccion == "Inicio":
    st.write(
        "El objetivo del proyecto es analizar los datos de la última campaña de"
        " una entidad financiera para descubrir relaciones y comportamientos"
        " relevantes entre las variables."
    )
    st.write("Alumno: Mario Alberto Ormeño Bobadilla")
    st.write("Especialización en Python for Analytics")
    st.write("2026")

# --- OPCIÓN 2: CARGA DEL DATASET ---
elif Seleccion == "Carga del dataset":
    st.header("Cargar el dataset")
    uploaded_file = st.file_uploader(
        "Seleccione un archivo CSV o XLSX", type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                try:
                    df = pd.read_csv(uploaded_file, sep=";")
                    if df.shape[1] <= 1:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, sep=",")
                except Exception:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)

            st.session_state["df"] = df  # Guardar en memoria
            st.success("¡Archivo cargado correctamente!")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vista previa (head):")
                st.dataframe(df.head())
            with col2:
                filas, columnas = df.shape
                st.subheader("Dimensiones:")
                st.write(f"• **Filas:** {filas:,}")
                st.write(f"• **Columnas:** {columnas}")

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

# --- OPCIÓN 3: EDA ---
elif Seleccion == "Análisis Exploratorio (EDA)":
    st.header("Análisis Exploratorio de Datos (EDA)")

    if st.session_state["df"] is None:
        st.warning(
            "Por favor, ve a la sección 'Carga del dataset' y sube un archivo"
            " primero."
        )
    else:
        df = st.session_state["df"]

        # Organización en Tabs (pestañas)
        tab1, tab2, tab3 = st.tabs(
            ["1. Info General", "2. Clasificación de Variables", "3. Más Ítems"]
        )

        # TAB 1: INFORMACIÓN GENERAL DEL DATASET
        with tab1:
            st.subheader("Ítem 1: Información general del dataset")
            st.write(
                "Resumen estructural de tipos de datos y valores faltantes del"
                " conjunto de datos."
            )

            # Reconstrucción de .info() en tabla formateada
            info_df = pd.DataFrame({
                "Tipo de Dato": df.dtypes.astype(str),
                "Valores Nulos": df.isnull().sum(),
                "% Nulos": (df.isnull().sum() / len(df) * 100).round(2),
            })

            col_a, col_b = st.columns([2, 1])

            with col_a:
                st.write("**Detalle de columnas y nulos:**")
                st.dataframe(info_df)

            with col_b:
                st.write("**Resumen de estado:**")
                st.metric("Total Filas", df.shape[0])
                st.metric("Total Columnas", df.shape[1])
                st.metric("Total Nulos", df.isnull().sum().sum())

        # TAB 2: CLASIFICACIÓN DE VARIABLES
        with tab2:
            st.subheader("Ítem 2: Clasificación de variables")
            st.write(
                "Identificación automática de variables numéricas y categóricas"
                " utilizando una función personalizada."
            )

            # Ejecutar función personalizada
            clasificacion = clasificar_variables(df)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Variables Numéricas", clasificacion["cant_numericas"]
                )
                st.write("**Listado de columnas numéricas:**")
                st.write(clasificacion["numericas"])

            with col2:
                st.metric(
                    "Variables Categóricas", clasificacion["cant_categoricas"]
                )
                st.write("**Listado de columnas categóricas:**")
                st.write(clasificacion["categoricas"])

        # TAB 3: ESPACIO PARA CONTINUAR LOS ÍTEMS DEL 3 AL 10
        with tab3:
            st.info("Aquí puedes ir añadiendo los Ítems 3 al 10 de tu proyecto.")