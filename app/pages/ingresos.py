
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

#### ayuda a visualizar todo en el apartado ingresos de la app


def show():
    st.title("Ingresos")

    # Cargar la base
    ruta_csv = Path(__file__).resolve().parents[1] / "recaudo_territorial.csv"
    df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # Limpiar texto en departamento y municipio
    df["departamento"] = df["departamento"].astype(str).str.strip()
    df["municipio"] = df["municipio"].astype(str).str.strip()

    # Crear filtros
    st.subheader("Filtros territoriales")

    departamentos = ["Todos"] + sorted(df["departamento"].dropna().unique().tolist())
    departamento_sel = st.selectbox("Departamento", departamentos)

    if departamento_sel == "Todos":
        municipios = ["Todos"] + sorted(df["municipio"].dropna().unique().tolist())
    else:
        municipios = ["Todos"] + sorted(
            df[df["departamento"] == departamento_sel]["municipio"].dropna().unique().tolist()
        )

    municipio_sel = st.selectbox("Municipio", municipios)

    #  Aplicar filtros
    df_filtrado = df.copy()

    if departamento_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["departamento"] == departamento_sel]

    if municipio_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["municipio"] == municipio_sel]


    # Preparar datos para gráficas
    df_graf = df_filtrado.copy()

    df_graf["año"] = pd.to_numeric(df_graf["año"], errors="coerce")
    df_graf["valor_recaudo"] = pd.to_numeric(df_graf["valor_recaudo"], errors="coerce")

    df_graf = df_graf.dropna(subset=["año", "valor_recaudo", "categoria"])

    if df_graf.empty:
        st.warning("No hay datos válidos para graficar.")
        return

    #  Gráficos principales
    st.write("## Histórico general")
    col1, col2 = st.columns(2)

    df_linea = df_graf.groupby("año", as_index=False)["valor_recaudo"].sum()

    fig_linea = px.line(
        df_linea,
        x="año",
        y="valor_recaudo",
        markers=True,
        title="Ingresos del territorio por año"
    )

    with col1:
        st.plotly_chart(fig_linea, use_container_width=True)

    df_barra = df_graf.groupby(["año", "categoria"], as_index=False)["valor_recaudo"].sum()

    fig_barra = px.bar(
        df_barra,
        x="año",
        y="valor_recaudo",
        color="categoria",
        barmode="stack",
        title="Composición del ingreso"
    )

    with col2:
        st.plotly_chart(fig_barra, use_container_width=True)

    # Top territorios
    st.write("## Top territorios")

    if departamento_sel == "Todos":
        df_top = df_graf.groupby("departamento", as_index=False)["valor_recaudo"].sum()
        df_top = df_top.sort_values("valor_recaudo", ascending=False).head(10)

        fig_top = px.bar(
            df_top,
            x="valor_recaudo",
            y="departamento",
            orientation="h",
            title="Top departamentos"
        )
    else:
        df_top = df_graf.groupby("municipio", as_index=False)["valor_recaudo"].sum()
        df_top = df_top.sort_values("valor_recaudo", ascending=False).head(10)

        fig_top = px.bar(
            df_top,
            x="valor_recaudo",
            y="municipio",
            orientation="h",
            title=f"Top municipios de {departamento_sel}"
        )

    fig_top.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_top, use_container_width=True)
        # histórico filtrado por territorio
    st.write("## Histórico filtrado por territorio")

    df_hist = df_filtrado.copy()

    df_hist["año"] = pd.to_numeric(df_hist["año"], errors="coerce")
    df_hist["valor_recaudo"] = pd.to_numeric(df_hist["valor_recaudo"], errors="coerce")

    df_hist = df_hist.dropna(subset=["año", "valor_recaudo", "tipo_recaudo"])

    if df_hist.empty:
        st.warning("No hay datos para este gráfico")
    else:
        tabla_hist = (
            df_hist.groupby(["año", "tipo_recaudo"])["valor_recaudo"]
            .sum()
            .unstack(fill_value=0)
            .sort_index()
        )

        st.line_chart(tabla_hist)


    

    

