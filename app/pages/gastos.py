import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

## ayuda a visualizar todo en el apartado gastos de la app
def show():
    st.title("Gastos")

    # -----------------------------
    # Barra interna de navegación
    # -----------------------------
    vista = st.radio(
        "Vista",
        ["General", "Por sector", "Por entidad"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # -----------------------------
    # Cargar base
    # -----------------------------
    ruta_csv = Path(__file__).resolve().parents[1] / "recaudo_territorial.csv"
    df = pd.read_csv(ruta_csv, sep=";", encoding="latin1")

    # -----------------------------
    # Limpiar columnas
    # -----------------------------
    df.columns = df.columns.str.strip()

    columnas_texto = [
        "departamento", "municipio", "region", "subregion",
        "categoria", "subcategoria", "sector", "tipo_recaudo",
        "fuente", "subfuente", "rubro", "subrubro",
        "programa", "subprograma", "proyecto",
        "gasto_programa", "gasto_subprograma", "gasto_proyecto", "gasto_proyecto.1",
        "entidad"
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    columnas_numericas = [
        "año", "mes", "trimestre", "semestre",
        "valor_recaudo", "presupuesto_inicial", "presupuesto_modificado",
        "meta_recaudo", "recaudo_acumulado", "ejecucion_%"
    ]

    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # Proxy monetario para gasto
    # -----------------------------
    valor_gasto = "presupuesto_modificado"

    if valor_gasto not in df.columns:
        st.error("No existe la columna 'presupuesto_modificado' en la base.")
        return

    # =========================================================
    # VISTA GENERAL
    # =========================================================
    if vista == "General":
        st.markdown("## Histórico general")

        # Filtros territoriales
        c1, c2 = st.columns(2)

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

        if df_filtrado.empty:
            st.warning("No hay datos con los filtros seleccionados.")
            return

        st.caption("Vista construida con presupuesto_modificado como proxy del gasto.")

        # 1) Apropiación histórica
        df_hist = (
            df_filtrado.groupby("año", as_index=False)[valor_gasto]
            .sum()
            .sort_values("año")
        )

        df_hist = df_hist.dropna(subset=["año", valor_gasto])

        if df_hist.empty:
            st.warning("No hay datos para la serie histórica de gasto.")
            return

        fig_hist = px.line(
            df_hist,
            x="año",
            y=valor_gasto,
            title="Apropiación histórica",
            markers=True
        )

        fig_hist.update_layout(
            xaxis_title="Año",
            yaxis_title="Presupuesto modificado",
            height=420
        )

        # 2) Composición del gasto (%)
        grupo_col = "gasto_programa"

        if grupo_col not in df_filtrado.columns:
            st.error("No existe la columna 'gasto_programa' en la base.")
            return

        df_comp = df_filtrado.copy()
        df_comp[grupo_col] = df_comp[grupo_col].replace(["", "nan", "None"], pd.NA)
        df_comp = df_comp.dropna(subset=[grupo_col, valor_gasto, "año"])

        if df_comp.empty:
            st.warning("No hay datos para la composición del gasto.")
            return

        top_n = 3
        top_grupos = (
            df_comp.groupby(grupo_col, as_index=False)[valor_gasto]
            .sum()
            .sort_values(valor_gasto, ascending=False)
            .head(top_n)[grupo_col]
            .tolist()
        )

        df_comp["grupo_plot"] = df_comp[grupo_col].where(
            df_comp[grupo_col].isin(top_grupos),
            "Otros"
        )

        df_comp_anual = (
            df_comp.groupby(["año", "grupo_plot"], as_index=False)[valor_gasto]
            .sum()
            .sort_values("año")
        )

        total_anual = df_comp_anual.groupby("año")[valor_gasto].transform("sum")
        df_comp_anual["porcentaje"] = (df_comp_anual[valor_gasto] / total_anual) * 100

        fig_comp = px.bar(
            df_comp_anual,
            x="año",
            y="porcentaje",
            color="grupo_plot",
            title="Composición del gasto (en %)"
        )

        fig_comp.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            legend_title="Gasto programa",
            barmode="stack",
            height=420
        )

        # 3) Gasto como % del total territorial
        df_total_territorio = (
            df_filtrado.groupby("año", as_index=False)[valor_gasto]
            .sum()
            .rename(columns={valor_gasto: "total_territorio"})
            .sort_values("año")
        )

        df_pct_territorio = df_comp_anual.merge(
            df_total_territorio,
            on="año",
            how="left"
        )

        df_pct_territorio["porcentaje_total"] = (
            df_pct_territorio[valor_gasto] / df_pct_territorio["total_territorio"]
        ) * 100

        fig_pct = px.bar(
            df_pct_territorio,
            x="año",
            y="porcentaje_total",
            color="grupo_plot",
            title="Gasto como % del total territorial"
        )

        fig_pct.update_layout(
            xaxis_title="Año",
            yaxis_title="Porcentaje",
            legend_title="Gasto programa",
            barmode="stack",
            height=420
        )

        # Mostrar las 3 gráficas en una sola fila
        col1, col2, col3 = st.columns(3)

        with col1:
            st.plotly_chart(
                fig_hist,
                use_container_width=True,
                key="gasto_historial_general"
            )

        with col2:
            st.plotly_chart(
                fig_comp,
                use_container_width=True,
                key="gasto_composicion_general"
            )

        with col3:
            st.plotly_chart(
                fig_pct,
                use_container_width=True,
                key="gasto_pct_total_general"
            )

    # =========================================================
    # VISTA POR SECTOR
    # =========================================================
    elif vista == "Por sector":
        st.markdown("## Gasto por sector")

        c1, c2, c3 = st.columns(3)

        with c1:
            departamentos = sorted(df["departamento"].dropna().astype(str).unique()) if "departamento" in df.columns else []
            departamento_sel = st.selectbox("Departamento", ["Todos"] + list(departamentos), key="sector_depto")

        df_filtrado = df.copy()

        if "departamento" in df_filtrado.columns and departamento_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["departamento"].astype(str) == departamento_sel]

        with c2:
            municipios = sorted(df_filtrado["municipio"].dropna().astype(str).unique()) if "municipio" in df_filtrado.columns else []
            municipio_sel = st.selectbox("Municipio", ["Todos"] + list(municipios), key="sector_mpio")

        if "municipio" in df_filtrado.columns and municipio_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["municipio"].astype(str) == municipio_sel]

        with c3:
            sectores = sorted(df_filtrado["sector"].dropna().astype(str).unique()) if "sector" in df_filtrado.columns else []
            sector_sel = st.selectbox("Sector", ["Todos"] + list(sectores), key="sector_sel")

        if "sector" in df_filtrado.columns and sector_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["sector"].astype(str) == sector_sel]

        if df_filtrado.empty:
            st.warning("No hay datos para los filtros seleccionados.")
            return

        df_sector = (
            df_filtrado.groupby("año", as_index=False)[valor_gasto]
            .sum()
            .sort_values("año")
        )

        fig_sector = px.line(
            df_sector,
            x="año",
            y=valor_gasto,
            title="Gasto por sector",
            markers=True
        )

        fig_sector.update_layout(
            xaxis_title="Año",
            yaxis_title="Presupuesto modificado",
            height=420
        )

        st.plotly_chart(fig_sector, use_container_width=True, key="graf_sector")

    # =========================================================
    # VISTA POR ENTIDAD
    # =========================================================
    else:
        st.markdown("## Gasto por entidad")

        c1, c2, c3 = st.columns(3)

        with c1:
            departamentos = sorted(df["departamento"].dropna().astype(str).unique()) if "departamento" in df.columns else []
            departamento_sel = st.selectbox("Departamento", ["Todos"] + list(departamentos), key="ent_depto")

        df_filtrado = df.copy()

        if "departamento" in df_filtrado.columns and departamento_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["departamento"].astype(str) == departamento_sel]

        with c2:
            municipios = sorted(df_filtrado["municipio"].dropna().astype(str).unique()) if "municipio" in df_filtrado.columns else []
            municipio_sel = st.selectbox("Municipio", ["Todos"] + list(municipios), key="ent_mpio")

        if "municipio" in df_filtrado.columns and municipio_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["municipio"].astype(str) == municipio_sel]

        with c3:
            entidades = sorted(df_filtrado["entidad"].dropna().astype(str).unique()) if "entidad" in df_filtrado.columns else []
            entidad_sel = st.selectbox("Entidad", ["Todos"] + list(entidades), key="entidad_sel")

        if "entidad" in df_filtrado.columns and entidad_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["entidad"].astype(str) == entidad_sel]

        if df_filtrado.empty:
            st.warning("No hay datos para los filtros seleccionados.")
            return

        df_entidad = (
            df_filtrado.groupby("año", as_index=False)[valor_gasto]
            .sum()
            .sort_values("año")
        )

        fig_entidad = px.line(
            df_entidad,
            x="año",
            y=valor_gasto,
            title="Gasto por entidad",
            markers=True
        )

        fig_entidad.update_layout(
            xaxis_title="Año",
            yaxis_title="Presupuesto modificado",
            height=420
        )

        st.plotly_chart(fig_entidad, use_container_width=True, key="graf_entidad")