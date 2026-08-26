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

        # Creación de pestañas para los Ítems 1 al 9
        (
            tab1,
            tab2,
            tab3,
            tab4,
            tab5,
            tab6,
            tab7,
            tab8,
            tab9,
        ) = st.tabs([
            "1. Info General",
            "2. Clasificación",
            "3. Estadísticas",
            "4. Faltantes",
            "5. Dist. Numérica",
            "6. Anál. Categórico",
            "7. Bivariado (Num vs Cat)",
            "8. Bivariado (Cat vs Cat)",
            "9. Análisis Dinámico",
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
            desc = df.describe().T
            if clasif["cant_numericas"] > 0:
                desc["mediana (50%)"] = df[clasif["numericas"]].median()
            st.dataframe(desc)

        # TAB 4: VALORES FALTANTES
        with tab4:
            st.subheader("Ítem 4: Análisis de valores faltantes")
            nulos_series = df.isnull().sum()
            df_nulos = pd.DataFrame(
                {"Columna": nulos_series.index, "Nulos": nulos_series.values}
            )
            df_nulos["% Nulos"] = (df_nulos["Nulos"] / len(df) * 100).round(2)
            df_nulos = df_nulos[df_nulos["Nulos"] > 0]

            if df_nulos.empty:
                st.success(
                    "¡El dataset no registra valores faltantes (nulos)!"
                )
            else:
                col_n1, col_n2 = st.columns([1, 2])
                with col_n1:
                    st.dataframe(df_nulos)
                with col_n2:
                    fig, ax = plt.subplots(figsize=(6, 3))
                    sns.barplot(
                        data=df_nulos, x="% Nulos", y="Columna", ax=ax
                    )
                    st.pyplot(fig)

        # TAB 5: DISTRIBUCIÓN NUMÉRICA
        with tab5:
            st.subheader("Ítem 5: Distribución de variables numéricas")
            if clasif["cant_numericas"] > 0:
                var_sel = st.selectbox(
                    "Selecciona una variable numérica:", clasif["numericas"]
                )
                fig, ax = plt.subplots(figsize=(7, 3))
                sns.histplot(df[var_sel], kde=True, ax=ax, color="skyblue")
                st.pyplot(fig)

        # TAB 6: ANÁLISIS DE VARIABLES CATEGÓRICAS
        with tab6:
            st.subheader("Ítem 6: Análisis de variables categóricas")
            if clasif["cant_categoricas"] > 0:
                var_cat = st.selectbox(
                    "Selecciona una variable categórica:", clasif["categoricas"]
                )

                # Conteos y Proporciones
                conteo = df[var_cat].value_counts()
                proporcion = df[var_cat].value_counts(normalize=True) * 100
                tabla_cat = pd.DataFrame(
                    {"Frecuencia Absoluta": conteo, "Porcentaje (%)": proporcion}
                )

                col_c1, col_c2 = st.columns([1, 2])
                with col_c1:
                    st.write("**Conteos y Proporciones:**")
                    st.dataframe(tabla_cat.round(2))

                with col_c2:
                    st.write("**Gráfico de Barras:**")
                    fig, ax = plt.subplots(figsize=(7, 3.5))
                    sns.barplot(
                        x=conteo.index,
                        y=conteo.values,
                        ax=ax,
                        palette="viridis",
                    )
                    plt.xticks(rotation=45)
                    ax.set_title(f"Distribución de {var_cat}")
                    st.pyplot(fig)
            else:
                st.info("No se encontraron variables categóricas.")

        # TAB 7: ANÁLISIS BIVARIADO (NUMÉRICO VS CATEGÓRICO)
        with tab7:
            st.subheader(
                "Ítem 7: Análisis bivariado (numérico vs categórico)"
            )
            if (
                clasif["cant_numericas"] > 0
                and clasif["cant_categoricas"] > 0
            ):
                col_biv1, col_biv2 = st.columns(2)
                with col_biv1:
                    var_num_b = st.selectbox(
                        "Variable Numérica (ej. age, duration):",
                        clasif["numericas"],
                        key="biv_num",
                    )
                with col_biv2:
                    var_cat_b = st.selectbox(
                        "Variable Categórica (ej. y):",
                        clasif["categoricas"],
                        key="biv_cat",
                    )

                col_g1, col_g2 = st.columns([2, 1])
                with col_g1:
                    fig, ax = plt.subplots(figsize=(7, 3.5))
                    sns.boxplot(
                        data=df,
                        x=var_cat_b,
                        y=var_num_b,
                        ax=ax,
                        palette="Set2",
                    )
                    ax.set_title(f"{var_num_b} según {var_cat_b}")
                    st.pyplot(fig)

                with col_g2:
                    st.write("**Resumen estadístico por grupo:**")
                    resumen_biv = df.groupby(var_cat_b)[var_num_b].describe()
                    st.dataframe(resumen_biv.round(2))

        # TAB 8: ANÁLISIS BIVARIADO (CATEGÓRICO VS CATEGÓRICO)
        with tab8:
            st.subheader(
                "Ítem 8: Análisis bivariado (categórico vs categórico)"
            )
            if clasif["cant_categoricas"] >= 2:
                col_c1_sel, col_c2_sel = st.columns(2)
                with col_c1_sel:
                    cat1 = st.selectbox(
                        "Categoría 1 (ej. education, contact):",
                        clasif["categoricas"],
                        key="cat1",
                    )
                with col_c2_sel:
                    cat2 = st.selectbox(
                        "Categoría 2 (ej. y):", clasif["categoricas"], key="cat2"
                    )

                # Tabla cruzada (Crosstab)
                crosstab_res = pd.crosstab(
                    df[cat1], df[cat2], normalize="index"
                ) * 100

                col_tab1, col_tab2 = st.columns([1, 2])
                with col_tab1:
                    st.write("**Proporciones por fila (%):**")
                    st.dataframe(crosstab_res.round(2))

                with col_tab2:
                    fig, ax = plt.subplots(figsize=(7, 3.5))
                    crosstab_res.plot(kind="bar", stacked=True, ax=ax, cmap="tab10")
                    ax.set_ylabel("Porcentaje (%)")
                    ax.set_title(f"Relación entre {cat1} y {cat2}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

        # TAB 9: ANÁLISIS BASADO EN PARÁMETROS SELECCIONADOS
        with tab9:
            st.subheader(
                "Ítem 9: Análisis basado en parámetros seleccionados"
            )
            st.write(
                "Filtra dinámicamente el dataset según las condiciones que"
                " elijas."
            )

            col_p1, col_p2 = st.columns(2)

            with col_p1:
                # Selector dinámico de columnas categóricas para filtrar
                col_filtro = st.selectbox(
                    "Selecciona una columna para filtrar:", clasif["categoricas"]
                )

            with col_p2:
                # Multiselect para elegir opciones específicas de esa columna
                opciones_disponibles = df[col_filtro].dropna().unique().tolist()
                opciones_sel = st.multiselect(
                    f"Selecciona valores de '{col_filtro}':",
                    options=opciones_disponibles,
                    default=opciones_disponibles[:2] if len(opciones_disponibles) >= 2 else opciones_disponibles,
                )

            # Filtrar DataFrame
            if opciones_sel:
                df_filtrado = df[df[col_filtro].isin(opciones_sel)]
            else:
                df_filtrado = df

            # Métricas dinámicas del filtro
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Registros Filtrados", f"{len(df_filtrado):,}")
            m2.metric(
                "% del Total",
                f"{(len(df_filtrado) / len(df) * 100):.2f}%",
            )
            m3.metric("Columnas", df_filtrado.shape[1])

            st.write("**Vista previa de los datos filtrados:**")
            st.dataframe(df_filtrado.head(10))