import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

def show():
    st.subheader("Recaudo histórico")

    vista = st.radio(
        "Vista",
        ["General", "Detallado"],
        horizontal=True,
        label_visibility="collapsed"
    )

    ruta_csv = Path(__file__).resolve().parents[1] / "recaudo_territorial.csv"
    df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

    df.columns = df.columns.str.strip()

    columnas_texto = [
        "departamento", "municipio", "region", "subregion",
        "categoria", "subcategoria", "sector", "tipo_recaudo",
        "fuente", "subfuente", "rubro", "subrubro"
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    columnas_numericas = [
        "año", "mes", "trimestre", "semestre",
        "valor_recaudo", "recaudo_acumulado",
        "presupuesto_inicial", "presupuesto_modificado",
        "meta_recaudo", "ejecucion_%"
    ]

    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if vista == "General":
        st.markdown("### Vista general")

        if "año" not in df.columns or "recaudo_acumulado" not in df.columns or "departamento" not in df.columns:
            st.error("Faltan columnas necesarias: año, recaudo_acumulado o departamento.")
            return

        # ---------------------------------
        # TOP departamentos para no saturar
        # ---------------------------------
        top_n = 6
        top_deptos = (
            df.groupby("departamento", as_index=False)["recaudo_acumulado"]
            .sum()
            .sort_values("recaudo_acumulado", ascending=False)
            .head(top_n)["departamento"]
            .tolist()
        )

        df_top = df.copy()
        df_top["departamento_plot"] = df_top["departamento"].where(
            df_top["departamento"].isin(top_deptos),
            "Otros"
        )

        # ---------------------------------
        # Gráfico 1: recaudo histórico total
        # ---------------------------------
        df_total = (
            df.groupby("año", as_index=False)["recaudo_acumulado"]
            .sum()
            .sort_values("año")
        )
        df_total = df_total.dropna(subset=["año", "recaudo_acumulado"])

        # ---------------------------------
        # Gráfico 2: % recaudo por departamento
        # ---------------------------------
        df_pct = (
            df_top.groupby(["año", "departamento_plot"], as_index=False)["recaudo_acumulado"]
            .sum()
            .sort_values("año")
        )
        total_anual = df_pct.groupby("año")["recaudo_acumulado"].transform("sum")
        df_pct["porcentaje"] = (df_pct["recaudo_acumulado"] / total_anual) * 100
        df_pct = df_pct.dropna(subset=["año", "porcentaje"])

        # ---------------------------------
        # Gráfico 3: participación promedio
        # ---------------------------------
        df_part = (
            df_top.groupby("departamento_plot", as_index=False)["recaudo_acumulado"]
            .sum()
            .sort_values("recaudo_acumulado", ascending=False)
        )
        total_general = df_part["recaudo_acumulado"].sum()
        df_part["participacion"] = (df_part["recaudo_acumulado"] / total_general) * 100

        # ---------------------------------
        # Crear figuras
        # ---------------------------------
        fig_total = px.area(
            df_total,
            x="año",
            y="recaudo_acumulado",
            title="Recaudo histórico total"
        )
        fig_total.update_layout(
            xaxis_title="Año",
            yaxis_title="Recaudo acumulado",
            height=360
        )

        fig_pct = px.area(
            df_pct,
            x="año",
            y="porcentaje",
            color="departamento_plot",
            title="% del recaudo por departamento"
        )
        fig_pct.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            legend_title="Departamento",
            height=360
        )

        fig_part = px.bar(
            df_part,
            x="departamento_plot",
            y="participacion",
            color="departamento_plot",
            title="Participación en el recaudo total"
        )
        fig_part.update_layout(
            xaxis_title="Departamento",
            yaxis_title="Participación (%)",
            showlegend=False,
            height=360
        )

        # ---------------------------------
        # Mostrar 3 juntas
        # ---------------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            st.plotly_chart(fig_total, use_container_width=True, key="recaudo_total_3")

        with c2:
            st.plotly_chart(fig_pct, use_container_width=True, key="recaudo_pct_3")

        with c3:
            st.plotly_chart(fig_part, use_container_width=True, key="recaudo_part_3")
                    # ---------------------------------
        # Treemap adicional debajo
        # ---------------------------------
        st.markdown("### Distribución del recaudo (treemap)")

        df_tree = (
            df.groupby(["departamento", "municipio"], as_index=False)["recaudo_acumulado"]
            .sum()
        )

        df_tree = df_tree.dropna(subset=["departamento", "municipio", "recaudo_acumulado"])

        if not df_tree.empty:
            fig_tree = px.treemap(
                df_tree,
                path=["departamento", "municipio"],
                values="recaudo_acumulado",
                color="recaudo_acumulado",
                title="Treemap del recaudo por departamento y municipio"
            )

            fig_tree.update_layout(
                height=650,
                margin=dict(t=50, l=10, r=10, b=10)
            )

            st.plotly_chart(
                fig_tree,
                use_container_width=True,
                key="treemap_recaudo_general_extra"
            )

    else:
        st.markdown("### Vista detallada")
        st.write("Recaudo por tipo de impuesto")
        

        # -----------------------------
        # Filtros
        # -----------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            departamentos = sorted(df["departamento"].dropna().astype(str).unique()) if "departamento" in df.columns else []
            departamento_sel = st.selectbox("Seleccione un departamento:", ["Todos"] + list(departamentos))

        df_filtrado = df.copy()
        if "departamento" in df_filtrado.columns and departamento_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["departamento"].astype(str) == departamento_sel]

        with c2:
            municipios = sorted(df_filtrado["municipio"].dropna().astype(str).unique()) if "municipio" in df_filtrado.columns else []
            municipio_sel = st.selectbox("Seleccione un municipio:", ["Todos"] + list(municipios))

        if "municipio" in df_filtrado.columns and municipio_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["municipio"].astype(str) == municipio_sel]

        with c3:
            impuestos = sorted(
                df_filtrado["impuesto_territorial"].dropna().astype(str).unique()
            ) if "impuesto_territorial" in df_filtrado.columns else []

            impuesto_sel = st.selectbox("Seleccione un impuesto:", impuestos)

        if "impuesto_territorial" in df_filtrado.columns:
            df_impuesto = df_filtrado[
                df_filtrado["impuesto_territorial"].astype(str) == impuesto_sel
            ].copy()
        else:
            st.error("No existe la columna 'impuesto_territorial' en la base.")
            return

        # -----------------------------
        # Validaciones
        # -----------------------------
        if df_impuesto.empty:
            st.warning("No hay datos para los filtros seleccionados.")
            return

        if "año" not in df_impuesto.columns or "recaudo_acumulado" not in df_impuesto.columns:
            st.error("Faltan columnas necesarias: 'año' o 'recaudo_acumulado'.")
            return

        # -----------------------------
        # Gráfico 1: Recaudo histórico del impuesto
        # -----------------------------
        df_hist = (
            df_impuesto.groupby("año", as_index=False)["recaudo_acumulado"]
            .sum()
            .sort_values("año")
        )

        df_hist = df_hist.dropna(subset=["año", "recaudo_acumulado"])

        # -----------------------------
        # Gráfico 2: % participación del impuesto
        # respecto al recaudo total del territorio filtrado
        # -----------------------------
        df_total_territorio = (
            df_filtrado.groupby("año", as_index=False)["recaudo_acumulado"]
            .sum()
            .rename(columns={"recaudo_acumulado": "recaudo_total_territorio"})
            .sort_values("año")
        )

        df_pct = df_hist.merge(df_total_territorio, on="año", how="left")
        df_pct["porcentaje"] = (
            df_pct["recaudo_acumulado"] / df_pct["recaudo_total_territorio"]
        ) * 100

        # -----------------------------
        # Títulos dinámicos
        # -----------------------------
        titulo_base = f"{impuesto_sel}"

        if departamento_sel != "Todos":
            titulo_base += f" - {departamento_sel}"

        if municipio_sel != "Todos":
            titulo_base += f" / {municipio_sel}"

        # -----------------------------
        # Figuras
        # -----------------------------
        fig_line = px.line(
            df_hist,
            x="año",
            y="recaudo_acumulado",
            title="Recaudo",
            markers=True
        )

        fig_line.update_layout(
            xaxis_title="Año",
            yaxis_title="Recaudo acumulado",
            height=420
        )

        fig_bar = px.bar(
            df_pct,
            x="año",
            y="porcentaje",
            title="Participación en el recaudo (%)"
        )

        fig_bar.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            height=420
        )

        # -----------------------------
        # Encabezado
        # -----------------------------
        st.caption(f"Filtro aplicado: {titulo_base}")

        # -----------------------------
        # Mostrar gráficos
        # -----------------------------
        g1, g2 = st.columns(2)

        with g1:
            st.plotly_chart(
                fig_line,
                use_container_width=True,
                key="recaudo_detallado_impuesto"
            )

        with g2:
            st.plotly_chart(
                fig_bar,
                use_container_width=True,
                key="recaudo_pct_detallado_impuesto"
            )
        
    