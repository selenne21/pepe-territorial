import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def show():
    st.title("Ejecución")

    # -----------------------------
    # Cargar base
    # -----------------------------
    ruta_csv = Path(__file__).resolve().parents[1] / "recaudo_territorial.csv"
    df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

    # -----------------------------
    # Limpiar nombres de columnas
    # -----------------------------
    df.columns = df.columns.str.strip()

    # -----------------------------
    # Limpiar texto
    # -----------------------------
    columnas_texto = [
        "departamento", "municipio", "sector", "categoria", "subcategoria",
        "tipo_recaudo", "fuente", "subfuente", "rubro", "subrubro",
        "programa", "subprograma", "proyecto"
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # -----------------------------
    # Convertir columnas numéricas
    # -----------------------------
    columnas_numericas = [
        "año",
        "recaudo_acumulado",
        "valor_recaudo",
        "presupuesto_inicial",
        "presupuesto_modificado",
        "ejecucion_%"
    ]

    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # Filtros territoriales generales
    # -----------------------------
    c1, c2 = st.columns(2)

    with c1:
        departamentos = sorted(df["departamento"].dropna().unique()) if "departamento" in df.columns else []
        departamento_sel = st.selectbox("Departamento", ["Todos"] + list(departamentos))

    if "departamento" in df.columns and departamento_sel != "Todos":
        df = df[df["departamento"] == departamento_sel]

    with c2:
        municipios = sorted(df["municipio"].dropna().unique()) if "municipio" in df.columns else []
        municipio_sel = st.selectbox("Municipio", ["Todos"] + list(municipios))

    if "municipio" in df.columns and municipio_sel != "Todos":
        df = df[df["municipio"] == municipio_sel]

    # -----------------------------
    # Filtrar 
    # -----------------------------
    columnas_busqueda = [
        "tipo_recaudo",
        "categoria",
        "subcategoria",
        "fuente",
        "subfuente",
        "rubro",
        "subrubro",
        "programa",
        "subprograma",
        "proyecto"
    ]

    mascara_deuda = pd.Series(False, index=df.index)

    for col in columnas_busqueda:
        if col in df.columns:
            mascara_deuda = mascara_deuda | df[col].astype(str).str.contains(
                "deuda", case=False, na=False
            )

    df_sin_deuda = df[~mascara_deuda].copy()

    if df_sin_deuda.empty:
        st.warning("No hay datos disponibles con los filtros seleccionados.")
        return

    grupo_col = "categoria"

    # =========================================================
    # 1. EJECUCIÓN HISTÓRICA  (GENERAL)
    # =========================================================
    st.subheader("Ejecución histórica")

    df_hist = (
        df_sin_deuda.groupby(["año", grupo_col], as_index=False)["recaudo_acumulado"]
        .sum()
        .sort_values("año")
    )

    df_hist = df_hist.dropna(subset=["año", "recaudo_acumulado"])

    if not df_hist.empty:
        fig_ejecucion = px.area(
            df_hist,
            x="año",
            y="recaudo_acumulado",
            color=grupo_col,
            title="Ejecución"
        )

        fig_ejecucion.update_layout(
            xaxis_title="Año",
            yaxis_title="Recaudo acumulado",
            legend_title="Categoría",
            height=420
        )

        df_pct = df_hist.copy()
        total_anual = df_pct.groupby("año")["recaudo_acumulado"].transform("sum")
        df_pct["porcentaje"] = (df_pct["recaudo_acumulado"] / total_anual) * 100

        fig_porcentaje = px.area(
            df_pct,
            x="año",
            y="porcentaje",
            color=grupo_col,
            title="%"
        )

        fig_porcentaje.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            legend_title="Categoría",
            height=420
        )

        g1, g2 = st.columns(2)

        with g1:
            st.plotly_chart(
                fig_ejecucion,
                use_container_width=True,
                key="graf_ejec_general"
            )

        with g2:
            st.plotly_chart(
                fig_porcentaje,
                use_container_width=True,
                key="graf_pct_general"
            )

    # =========================================================
    # 2. EJECUCIÓN HISTÓRICA POR SECTOR 
    # =========================================================
    st.subheader("Ejecución histórica por sector")

    if "sector" in df_sin_deuda.columns:
        df_sin_deuda["sector"] = df_sin_deuda["sector"].replace(["", "nan", "None"], pd.NA)
        sectores = sorted(df_sin_deuda["sector"].dropna().unique())
    else:
        sectores = []

    sector_sel = st.selectbox("Seleccione el sector:", ["Todos"] + list(sectores))

    df_sector = df_sin_deuda.copy()

    if "sector" in df_sector.columns and sector_sel != "Todos":
        df_sector = df_sector[df_sector["sector"] == sector_sel]

    if df_sector.empty:
        st.warning("No hay datos para el sector seleccionado.")
        return

    df_hist_sector = (
        df_sector.groupby(["año", grupo_col], as_index=False)["recaudo_acumulado"]
        .sum()
        .sort_values("año")
    )

    df_hist_sector = df_hist_sector.dropna(subset=["año", "recaudo_acumulado"])

    if not df_hist_sector.empty:
        fig_ejecucion_sector = px.area(
            df_hist_sector,
            x="año",
            y="recaudo_acumulado",
            color=grupo_col,
            title="Ejecución"
        )

        fig_ejecucion_sector.update_layout(
            xaxis_title="Año",
            yaxis_title="Recaudo acumulado",
            legend_title="Categoría",
            height=420
        )

        df_pct_sector = df_hist_sector.copy()
        total_anual_sector = df_pct_sector.groupby("año")["recaudo_acumulado"].transform("sum")
        df_pct_sector["porcentaje"] = (df_pct_sector["recaudo_acumulado"] / total_anual_sector) * 100

        fig_porcentaje_sector = px.area(
            df_pct_sector,
            x="año",
            y="porcentaje",
            color=grupo_col,
            title="%"
        )

        fig_porcentaje_sector.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            legend_title="Categoría",
            height=420
        )

        s1, s2 = st.columns(2)

        with s1:
            st.plotly_chart(
                fig_ejecucion_sector,
                use_container_width=True,
                key="graf_ejec_sector"
            )

        with s2:
            st.plotly_chart(
                fig_porcentaje_sector,
                use_container_width=True,
                key="graf_pct_sector"
            )