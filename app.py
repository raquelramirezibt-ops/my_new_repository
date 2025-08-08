import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Carga y limpieza de datos
# -----------------------------
car_data = pd.read_csv("vehicles_us.csv")
car_data = car_data.dropna(
    subset=["model_year", "odometer", "price", "condition", "fuel"]
)

# -----------------------------
# Título y encabezado
# -----------------------------
st.title("Análisis interactivo de anuncios de coches")
st.header("Panel de análisis de anuncios de venta de coches")

# Vista previa
st.subheader("Vista previa de los datos")
st.write(car_data.head())
st.markdown("---")

# -----------------------------
# Filtros (sidebar)
# -----------------------------
st.sidebar.header("Filtros")

selected_conditions = st.sidebar.multiselect(
    "Selecciona el estado del coche",
    options=sorted(car_data["condition"].dropna().unique()),
    default=sorted(car_data["condition"].dropna().unique()),
)

selected_fuel = st.sidebar.multiselect(
    "Tipo de combustible",
    options=sorted(car_data["fuel"].dropna().unique()),
    default=sorted(car_data["fuel"].dropna().unique()),
)

min_year = int(car_data["model_year"].min())
max_year = int(car_data["model_year"].max())

selected_years = st.sidebar.slider(
    "Selecciona el rango de años del modelo",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

# -----------------------------
# Filtrado
# -----------------------------
filtered_data = car_data[
    (car_data["condition"].isin(selected_conditions))
    & (car_data["fuel"].isin(selected_fuel))
    & (car_data["model_year"] >= selected_years[0])
    & (car_data["model_year"] <= selected_years[1])
]

# -----------------------------
# Resultados
# -----------------------------
if not filtered_data.empty:
    # KPIs
    st.subheader("Resumen general")
    col1, col2, col3 = st.columns(3)
    col1.metric("Precio promedio", f"${filtered_data['price'].mean():,.0f}")
    col2.metric("Kilometraje promedio", f"{filtered_data['odometer'].mean():,.0f} km")
    col3.metric("Cantidad de vehículos", len(filtered_data))

    st.markdown("---")

    # --- Controles para mostrar/ocultar gráficos ---
    st.subheader("Gráficos")
    colA, colB, colC, colD = st.columns(4)
    show_hist = colA.checkbox("Histograma", value=True)
    show_scatter = colB.checkbox("Dispersión", value=True)
    show_bars = colC.checkbox("Barras por tipo", value=True)
    show_box = colD.checkbox("Boxplot por condición", value=True)

    st.markdown("---")

    # --- Histograma ---
    if show_hist:
        st.subheader("Histograma del odómetro")
        fig_hist = px.histogram(filtered_data, x="odometer")
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- Dispersión ---
    if show_scatter:
        st.subheader("Gráfico de dispersión: precio vs año del modelo")
        fig_scatter = px.scatter(
            filtered_data,
            x="model_year",
            y="price",
            color="condition",
            hover_data=["model", "type"],
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Barras por tipo ---
    if show_bars:
        st.subheader("Gráfico de barras: cantidad de coches por tipo")
        df_bar = (
            filtered_data["type"].value_counts()
            .rename_axis("type")
            .reset_index(name="count")
        )
        fig_bar = px.bar(
            df_bar,
            x="type",
            y="count",
            labels={"type": "Tipo", "count": "Cantidad"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Boxplot por condición ---
    if show_box:
        st.subheader("Distribución de precios por condición")
        fig_box = px.box(filtered_data, x="condition", y="price")
        st.plotly_chart(fig_box, use_container_width=True)

    # --- Tabla expandible ---
    with st.expander("Ver tabla completa de datos filtrados"):
        st.dataframe(filtered_data)

else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")