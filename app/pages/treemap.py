import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def show():

    st.title("Treemap Territorial")

    # ---------------- SELECTOR ----------------
    opcion = st.radio(
        "Seleccione vista",
        ["Ingresos", "Gastos"],
        horizontal=True
    )

    # ---------------- CARGAR DATA ----------------
    ruta_csv = Path(__file__).resolve().parents[1] / "recaudo_territorial.csv"
    df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

    # ---------------- LIMPIEZA ----------------
    df["año"] = pd.to_numeric(df["año"], errors="coerce")
    df["valor_recaudo"] = pd.to_numeric(df["valor_recaudo"], errors="coerce")
    df["categoria"] = df["categoria"].astype(str).str.lower().str.strip()

    # 🔴 VER CATEGORÍAS REALES
    categorias = df["categoria"].dropna().unique()
    st.write("Categorías en tu base:", categorias)

    # ---------------- DEFINIR GASTOS MANUAL ----------------
    categorias_gasto = st.multiselect(
        "Seleccione qué categorías",
        categorias
    )

    if len(categorias_gasto) == 0:
        st.warning("Seleccione al menos una categoría")
        return

    # ---------------- CLASIFICACIÓN ----------------
    df_gastos = df[df["categoria"].isin(categorias_gasto)]
    df_ingresos = df[~df["categoria"].isin(categorias_gasto)]

    # ---------------- SELECCIÓN ----------------
    if opcion == "Ingresos":
        df_filtrado = df_ingresos
        color = "Blues"
        st.subheader("Treemap de Ingresos")

    else:
        df_filtrado = df_gastos
        color = "Reds"
        st.subheader("Treemap de Gastos")

    # ---------------- VALIDAR ----------------
    if df_filtrado.empty:
        st.error("No hay datos en esta categoría")
        return

    df_filtrado = df_filtrado.dropna(subset=["año"])

    # ---------------- SLIDER ----------------
    año = st.slider(
        "Seleccione el año",
        int(df_filtrado["año"].min()),
        int(df_filtrado["año"].max()),
        int(df_filtrado["año"].min())
    )

    df_filtrado = df_filtrado[df_filtrado["año"] == año]

    if df_filtrado.empty:
        st.warning("No hay datos para ese año")
        return

    # ---------------- AGRUPACIÓN ----------------
    df_group = df_filtrado.groupby(
        ["pais", "region", "departamento", "municipio"],
        as_index=False
    )["valor_recaudo"].sum()

    # ---------------- TREEMAP ----------------
    fig = px.treemap(
        df_group,
        path=["pais", "region", "departamento", "municipio"],
        values="valor_recaudo",
        color="valor_recaudo",
        color_continuous_scale=color
    )

    st.plotly_chart(fig, use_container_width=True)