import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="PROYECTO - BankMarketing", layout="wide")

st.title("PROYECTO - BankMarketing")
st.sidebar.title("Menú de navegación")


# Función personalizada para clasificar variables
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

            st.session_state["df"] = df
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
        clasif = clasificar_variables(df)

        # Creación de pestañas para los ítems 1 al 5
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "1. Info General",
            "2. Clasificación",
            "3. Estadísticas Descriptivas",
            "4. Valores Faltantes",
            "5. Distribución Numérica",
        ])

        # TAB 1: INFORMACIÓN GENERAL
        with tab1:
            st.subheader("Ítem 1: Información general del dataset")
            info_df = pd.DataFrame({
                "Tipo de Dato": df.dtypes.astype(str),
                "Valores Nulos": df.isnull().sum(),
                "% Nulos": (df.isnull().sum() / len(df) * 100).round(2),
            })
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.dataframe(info_df)
            with col_b:
                st.metric("Total Filas", df.shape[0])
                st.metric("Total Columnas", df.shape[1])
                st.metric("Total Nulos", df.isnull().sum().sum())

        # TAB 2: CLASIFICACIÓN DE VARIABLES
        with tab2:
            st.subheader("Ítem 2: Clasificación de variables")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Variables Numéricas", clasif["cant_numericas"])
                st.write(clasif["numericas"])
            with col2:
                st.metric("Variables Categóricas", clasif["cant_categoricas"])
                st.write(clasif["categoricas"])

        # TAB 3: ESTADÍSTICAS DESCRIPTIVAS
        with tab3:
            st.subheader("Ítem 3: Estadísticas descriptivas")
            st.write(
                "Resumen de medidas de tendencia central y dispersión mediante"
                " `.describe()`."
            )

            desc = df.describe().T
            desc["mediana (50%)"] = df[clasif["numericas"]].median()

            st.dataframe(desc)

            col_e1, col_e2 = st.columns(2)
            with col_e1:
                st.info(
                    "**Medias vs Medianas:**\nSi la media supera con creces"
                    " a la mediana, la variable presenta sesgo positivo por"
                    " presencia de valores atípicos elevados."
                )
            with col_e2:
                st.info(
                    "**Dispersión (std):**\nUna desviación estándar amplia"
                    " indica alta variabilidad de los datos respecto a su"
                    " valor promedio."
                )

        # TAB 4: ANÁLISIS DE VALORES FALTANTES
        with tab4:
            st.subheader("Ítem 4: Análisis de valores faltantes")

            nulos_series = df.isnull().sum()
            df_nulos = pd.DataFrame(
                {"Columna": nulos_series.index, "Nulos": nulos_series.values}
            )
            df_nulos["% Nulos"] = (df_nulos["Nulos"] / len(df) * 100).round(2)
            df_nulos = df_nulos[df_nulos["Nulos"] > 0].sort_values(
                by="Nulos", ascending=False
            )

            if df_nulos.empty:
                st.success(
                    "¡El dataset no registra valores faltantes (nulos)!"
                )
            else:
                col_n1, col_n2 = st.columns([1, 2])
                with col_n1:
                    st.write("**Conteo de nulos:**")
                    st.dataframe(df_nulos)

                with col_n2:
                    st.write("**Visualización:**")
                    fig, ax = plt.subplots(figsize=(6, 3))
                    sns.barplot(
                        data=df_nulos,
                        x="% Nulos",
                        y="Columna",
                        palette="Reds_r",
                        ax=ax,
                    )
                    ax.set_title("Porcentaje de Nulos por Variable")
                    st.pyplot(fig)

            st.markdown(
                "**Discusión breve:** Los datos faltantes en campañas bancarias"
                " suelen originarse por campos opcionales en el registro de"
                " clientes o fallas en el almacenamiento de interacciones."
            )

        # TAB 5: DISTRIBUCIÓN DE VARIABLES NUMÉRICAS
        with tab5:
            st.subheader("Ítem 5: Distribución de variables numéricas")

            if clasif["cant_numericas"] > 0:
                var_sel = st.selectbox(
                    "Selecciona una variable numérica:", clasif["numericas"]
                )
                bins_val = st.slider("Número de barras (bins):", 5, 50, 20)

                col_g1, col_g2 = st.columns([2, 1])

                with col_g1:
                    fig, ax = plt.subplots(figsize=(7, 3.5))
                    sns.histplot(
                        df[var_sel],
                        bins=bins_val,
                        kde=True,
                        color="royalblue",
                        edgecolor="black",
                        ax=ax,
                    )
                    ax.set_title(f"Histograma y curva KDE de: {var_sel}")
                    st.pyplot(fig)

                with col_g2:
                    st.write("**Interpretación visual:**")
                    med = df[var_sel].mean()
                    medn = df[var_sel].median()
                    std_v = df[var_sel].std()

                    st.write(f"• **Media:** {med:.2f}")
                    st.write(f"• **Mediana:** {medn:.2f}")
                    st.write(f"• **Desv. Estándar:** {std_v:.2f}")

                    if abs(med - medn) < (0.1 * std_v):
                        st.success("Distribución con tendencia simétrica.")
                    elif med > medn:
                        st.warning("Sesgo a la derecha (valores altos).")
                    else:
                        st.info("Sesgo a la izquierda (valores bajos).")
            else:
                st.warning("No hay variables numéricas en este dataset.")