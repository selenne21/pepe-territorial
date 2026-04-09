##PEPE TERRITORIAL
# Cargar librerias
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
#
st.set_page_config(layout="wide")
st.title("PEPE Territorial") 
#Menu lateral
menu=st.sidebar.radio("Navegación",["Main","Ingresos","Gastos","Coyuntura","Treemap","Presupuesto actual","Descarga de datos"])
#Que el menu cambie segun la selección


#Inicio
if menu=="Main":
    st.header("Main")

#Ingresos
elif  menu=="Ingresos":
    st.header("Ingresos")
    tab1, tab2,tab3=st.tabs(["General","Departamental","Municipal"])
    with tab1:
        #################GENERAL################################################
        ##Gráfica del historico
        st.subheader("Histórico general")
        st.caption("Cifras en miles de millones de pesos")
        df=pd.read_parquet("data/ing.parquet")
        ## las graficas se vean una al lado de la otra
        col1, col2=st.columns(2)
        ##agrupe los datos  por año para hacer la grafica 
        with col1:
          agrupamiento_año=df.groupby("Año")["TotalRecaudo"].sum().reset_index()
          agrupamiento_año["Total_mm"]=agrupamiento_año["TotalRecaudo"]/1_000_000_000
          fig=px.line(agrupamiento_año,x="Año",y="Total_mm", markers=True)
          fig.update_yaxes(title=None)
          st.plotly_chart(fig)
          ##############################################################################

        with col2:
           
           ## vamos a clafificar de otra manera los ingresos de la clasificacion general para que sea mas facil la visualización
           df["clasificacion_limpia"]="Otros"
           df.loc[df["clasificacion_ofpuj"].str.contains("TRANSFER",case=False,na=False),"clasificacion_limpia"]="Transferencias"
           df.loc[df["clasificacion_ofpuj"].str.contains("IMPUEST|TRIBUT",case=False,na=False),"clasificacion_limpia"]="Impuestos"
           df.loc[df["clasificacion_ofpuj"].str.contains("MULTA|SANCION",case=False,na=False),"clasificacion_limpia"]="Multas y sanciones"
           df.loc[df["clasificacion_ofpuj"].str.contains("CONTRIBU",case=False,na=False),"clasificacion_limpia"]="Contribuciones"
           df.loc[df["clasificacion_ofpuj"].str.contains("CAPITAL",case=False,na=False),"clasificacion_limpia"]="Recursos de capital"
           ## Gráfica de barras apiladas del ingreso clasificación normalita
           agrupar_barras_api=df.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
           agrupar_barras_api["Total_año"]=agrupar_barras_api.groupby("Año")["TotalRecaudo"].transform("sum")
           agrupar_barras_api["Porcentaje"]=agrupar_barras_api["TotalRecaudo"]/agrupar_barras_api["Total_año"]*100
           ##Gráfica de barras apiladas
           fig_barras=px.bar(
               agrupar_barras_api,
               x=("Año"),
               y=("Porcentaje"),
               color=("clasificacion_limpia"),
               barmode="stack"
           )
           fig_barras.update_yaxes(title=None)
           fig_barras.update_layout(legend_title=None)
           fig_barras.update_xaxes(tickmode="linear",dtick=2)
           fig_barras.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.2,
                   xanchor="left",
                   x=0
               )
           )
           st.plotly_chart(fig_barras,use_container_width=True)
        #################################FUERA COL1 Y COL2###########################
        ## Gráfica de area apilada con clasificación del observatorio
        ## agrupamos las variables
        area_df=df.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
        area_df["Total_anual_area1"]=area_df.groupby("Año")["TotalRecaudo"].transform("sum")###
        area_df["Porcentaje_area1"]= area_df["TotalRecaudo"]/area_df["Total_anual_area1"]###
        ##Gráfica area apilada
        fig_area_api=px.area(
            area_df,
            x="Año",
            y="Porcentaje_area1",
            color="clas_gen"
         )
        fig_area_api.update_yaxes(title=None)
        fig_area_api.update_yaxes(tickformat=".0%")
        fig_area_api.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_api.update_layout(legend_title=None)
        fig_area_api.update_layout(
            legend_title=None,
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.2,
                 xanchor="left",
                 x=0
               )
                  
           )
        st.plotly_chart(fig_area_api,use_container_width=True)

        #########################################################################
        ###############################SGP_GENERAL##############################
        st.subheader("Sistema General de Participaciones (SGP)")
        BASE_DIR = Path(__file__).resolve().parent.parent
        RUTA_SGP = BASE_DIR / "data" / "datos_sgp_pib_ic.parquet"
        df_sgp = pd.read_parquet(RUTA_SGP)
       ###listo ya cargada la primera base hagamos la primera grafica
       ## como hay muchas categorias me quedare con col1 la principal
        col1, col2=st.columns(2)
        ###############################COL1_sgp###############################################
        with col1:
        ####revisar
            sgp_total = (
            df_sgp.groupby("Año", as_index=False)["valor_constante_25"].sum()
            )
            sgp_total["valor_mm"] = sgp_total["valor_constante_25"] / 1_000_000_000
            sgp_total = sgp_total[
             (sgp_total["Año"] >= 2012) & (sgp_total["Año"] <= 2024)
            ]
            fig_sgp_2 = px.line(
                 sgp_total,
                 x="Año",
                 y="valor_mm",
                 markers=True
                )
            fig_sgp_2.update_yaxes(title=None)
            st.plotly_chart(fig_sgp_2, use_container_width=True)
        #######################COL2_sgp##########################################################
        with col2:
            ##grafico barras apiladas
            ## solo renombre
            df_sgp["clasificacion_sgp"] = df_sgp["nivel_1"]
            df_sgp["clasificacion_sgp"] = df_sgp["clasificacion_sgp"].replace({
            "Agua Potable": "Agua y saneamiento básico",
            "Propósito General": "Inversiones con propósito general"
            })
            ##filtro los años que estoy teniendo en cuenta
            df_sgp_filtrado = df_sgp[(df_sgp["Año"] >= 2012) & (df_sgp["Año"] <= 2024)
            ].copy()
            ## agrupo lo que me interesa
            barra_sgp = (
            df_sgp_filtrado.groupby(["Año", "clasificacion_sgp"], as_index=False)["valor_constante_25"].sum()
            )
            #columna total
            barra_sgp["total_año"] = barra_sgp.groupby("Año")["valor_constante_25"].transform("sum")
            #columna porcentaje
            barra_sgp["porcentaje"] = (
            barra_sgp["valor_constante_25"] / barra_sgp["total_año"]
            ) * 100
            ## genera un orden para cada año
            orden = [
                "Educación",
                "Salud",
                "Agua y saneamiento básico",
                "Inversiones con propósito general",
                "Asignaciones especiales"
                ]

            barra_sgp["clasificacion_sgp"] = pd.Categorical(
            barra_sgp["clasificacion_sgp"],
                categories=orden,
                ordered=True
            )
            ## ordena segun los años 
            barra_sgp = barra_sgp.sort_values(["Año", "clasificacion_sgp"])
            ##Gráfica barras apiladas
            fig_barra_sgp = px.bar(
                barra_sgp,
                x="Año",
                y="porcentaje",
                color="clasificacion_sgp",
                barmode="stack"
            )
            fig_barra_sgp.update_yaxes(title=None)
            fig_barra_sgp.update_layout(legend_title=None)
            fig_barra_sgp.update_xaxes(tickmode="linear",dtick=2)
            fig_barra_sgp.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.2,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart(fig_barra_sgp, use_container_width=True)
       
         #############FUERA COL1 Y COL2 SGP##############################################
         ##puse el nivel 1 en como otra variable/Grafica area
        df_sgp["clasificacion_sgp"] = df_sgp["nivel_1"]
        ##cambie noombres
        df_sgp["clasificacion_sgp"] = df_sgp["clasificacion_sgp"].replace({
         "Agua Potable": "Agua y saneamiento básico",
        "Propósito General": "Inversiones con propósito general"
        })
        ##filtro mis años
        df_sgp_filtrado = df_sgp[
        (df_sgp["Año"] >= 2012) & (df_sgp["Año"] <= 2024)
        ].copy()
        area_sgp = (
        df_sgp_filtrado.groupby(["Año", "clasificacion_sgp"], as_index=False)["valor_constante_25"] .sum()
        ) 
        area_sgp["total_año"] = area_sgp.groupby("Año")["valor_constante_25"].transform("sum")
        area_sgp["porcentaje"] = (area_sgp["valor_constante_25"] / area_sgp["total_año"]) * 100
        orden_sgp = [
            "Educación",
            "Salud",
            "Agua y saneamiento básico",
            "Inversiones con propósito general",
            "Asignaciones especiales"
        ]
        area_sgp["clasificacion_sgp"] = pd.Categorical(area_sgp["clasificacion_sgp"], categories=orden_sgp,ordered=True
        )

        area_sgp = area_sgp.sort_values(["Año", "clasificacion_sgp"])
        ##Gráfica area apilada
        fig_area_sgp = px.area(
            area_sgp,
            x="Año",
            y="porcentaje",
            color="clasificacion_sgp"
        )
        fig_area_sgp.update_yaxes(title=None)
        fig_area_sgp.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_sgp.update_layout(legend_title=None)
        fig_area_sgp.update_layout(
            legend_title=None,
            legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.2,
                 xanchor="left",
                 x=0
               )
                  
           )
        st.plotly_chart(fig_area_sgp,use_container_width=True)

        ###############################################################################################
        ##Treemap 
        ##titulo
        st.subheader("Asignación del SGP por categoría")
        ##Primero el filtro de año
        año_sgp = st.slider(
         "Seleccione el año",
            min_value=2012,
            max_value=2024,
            value=2012,
            step=1,
            key="slider_treemap_sgp"
        )
        ##hacemos filtro para años necesitamos
        ##que el año seleccionado sea igual al del SGP
        df_sgp_año = df_sgp[df_sgp["Año"] == año_sgp].copy()
        ##cambiar los nombres a unos mas apropiados
        df_sgp_año["categoria_sgp"] = df_sgp_año["nivel_1"].replace({
        "Agua Potable": "Agua y saneamiento básico",
        "Propósito General": "Inversiones con propósito general"
        })
        ###genere la profundidad con nivel_2
        df_sgp_año["subcategoria_sgp"] = df_sgp_año["nivel_2"].fillna("Sin detalle")
        ##agrupe las columnas que me interesan
        treemap_sgp = (df_sgp_año.groupby( ["categoria_sgp", "subcategoria_sgp"],as_index=False)["valor_constante_25"].sum())
        treemap_sgp["valor_mm"] = treemap_sgp["valor_constante_25"] / 1_000_000_000
        ##Gráfica
        treemap_fig_sgp = px.treemap(
            treemap_sgp,
            path=["categoria_sgp", "subcategoria_sgp"],
            values="valor_mm"
        )
        ##estetica
        treemap_fig_sgp.update_layout(margin=dict(t=40, l=10, r=10, b=10))##visual
        treemap_fig_sgp.update_traces(textinfo="label+percent entry")#muestra texto y porcentaje
        treemap_fig_sgp.update_traces(
            textfont=dict(
            size=16,
            color="white"
         )
         )#letra
        treemap_fig_sgp.update_traces(
            marker=dict(
            line=dict(width=4, color="white")
        )
        )##bordes
        st.plotly_chart(
        treemap_fig_sgp,use_container_width=True,key="treemap_sgp_general")    
        #########################################################################
        ##Nuevo gráfico de linea SGP/PIB SGP/IC 
        #titulo 
        st.subheader("Participación del SGP en el PIB y en los ingresos corrientes")
        ##filtro
        linea = df_sgp[  (df_sgp["Año"] >= 2012) & (df_sgp["Año"] <= 2024)].groupby("Año", as_index=False)[
         ["valor_sgp_pib", "valor_sgp_ingresos_corrientes"]
        ].sum()
        ##Cambie el nombre de los ejes
        linea = linea.rename(columns={
           "valor_sgp_pib": "SGP / PIB",
           "valor_sgp_ingresos_corrientes": "SGP / Ingresos Corrientes"
        })

        fig_linea_sgp = px.line(
        linea,
        x="Año",
        y=["SGP / PIB", "SGP / Ingresos Corrientes"],
        markers=True
        )

        fig_linea_sgp.update_yaxes(tickformat=".4%")

        st.plotly_chart(fig_linea_sgp, use_container_width=True)
        ##Quitar titulos de los ejes
        fig_linea_sgp.update_xaxes(title=None)
        fig_linea_sgp.update_yaxes(title=None)
        
       
########################DEPARTAMENTAL#########################################
    with tab2:
        departamentos=sorted(df["Departamento"].dropna().unique())
        seleccionar_depto=st.selectbox("Seleccione un Departamento",departamentos)
        st.caption("Cifras en miles de millones de pesos")
        col1,col2=st.columns(2)
        with col1:
           ##Gráfica general con filtro
           depto_filtrado=df[df["Departamento"]==seleccionar_depto]
           agrupar_depto=depto_filtrado.groupby("Año")["TotalRecaudo"].sum().reset_index()
           agrupar_depto["Total_mm"]= agrupar_depto["TotalRecaudo"]/1_000_000_000
           agrupar_depto = agrupar_depto.sort_values("Año")###cambio_deptos
           fig_gen_depto=px.line(
               agrupar_depto,
               x="Año",
               y="Total_mm",
               markers=True

            )
           fig_gen_depto.update_yaxes(title=None)
           fig_gen_depto.update_xaxes(tickmode="linear",dtick=2)########
           st.plotly_chart(fig_gen_depto)
           
           ######################################################################
        with col2:
            agrupar_depto_barrasapi=depto_filtrado.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
            agrupar_depto_barrasapi["Total_año_dep"]=agrupar_depto_barrasapi.groupby("Año")["TotalRecaudo"].transform("sum")
            agrupar_depto_barrasapi["Porcentaje_dpto"]= agrupar_depto_barrasapi["TotalRecaudo"]/ agrupar_depto_barrasapi["Total_año_dep"]*100
            agrupar_depto_barrasapi = agrupar_depto_barrasapi.groupby("Año").filter(
              lambda x: x["Porcentaje_dpto"].sum() > 0####no deja ver cosas que esten en 0
)
            agrupar_depto_barrasapi= agrupar_depto_barrasapi.sort_values("Año")#############################ordeno mis años
            años_dep = sorted(agrupar_depto_barrasapi["Año"].unique())##################################ordeno mis ejes del grafico
            fig_dep_depto=px.bar(
                agrupar_depto_barrasapi,
                x="Año",
                y="Porcentaje_dpto",
                color="clasificacion_limpia",
                barmode="stack"

         )
            fig_dep_depto.update_yaxes(title=None)
            fig_dep_depto.update_xaxes(
                 type="category",
                 categoryorder="array",
                 categoryarray=años_dep
                 )#################################### 
            fig_dep_depto.update_layout(legend_title=None)
            fig_dep_depto.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.15,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart(fig_dep_depto)
     ######################################FUERA COL1 Y COL2###################################################       
     ##Gráfica area 
        area_dep=depto_filtrado.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
        area_dep["Total_area2"]=area_dep.groupby("Año")["TotalRecaudo"].transform("sum")
        area_dep["Porcentaje_area2"]=area_dep["TotalRecaudo"]/area_dep["Total_area2"]
        fig_are_dep=px.area(
            area_dep,
            x="Año",
            y="Porcentaje_area2",
            color="clas_gen"
        )
        fig_are_dep.update_yaxes(title=None)
        fig_are_dep.update_yaxes(tickformat=".0%")
        fig_are_dep.update_xaxes(
        tickmode="array",
        tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
        ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
        range=[2011.8, 2024.8]
        )
        fig_are_dep.update_layout(legend_title=None)
        fig_are_dep.update_layout(
           legend_title=None,
           legend=dict(
               orientation="h",
               yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
            )
                  
           )
        st.plotly_chart(fig_are_dep,use_container_width=True)
        #########################SGP DEPARTAMENTAL#########################################
        ##################################################################################
        #selector de año
        st.subheader("Sistema General de Participaciones (SGP)")###
        año_sgp_dep=st.slider(
            "Seleccione el año",
            int(depto_filtrado["Año"].min()),
            int(depto_filtrado["Año"].max()),
            int(depto_filtrado["Año"].min()),
            key="slider_sgp_depto"
        )
        fil_año_depto=depto_filtrado[depto_filtrado["Año"]==año_sgp_dep].copy()
        df_sgp_depto=fil_año_depto[
            (
        fil_año_depto["clasificacion_ofpuj"].astype(str).str.strip().str.upper()
        =="SISTEMA GENERAL DE PARTICIPACIONES"
        )
        |
        (
             fil_año_depto["col_5"].astype(str).str.upper().str.contains(
                 "PARTICIPACIONES", na=False
             )
        )
        ].copy()

        def clasificar_cate_sgp_dep(valor):
            valor=str(valor).strip().upper()
            if "EDUCACION" in valor or "EDUCACIÓN" in valor:
                 return "Educación"
            elif "SALUD" in valor:
                 return "Salud"
            elif "AGUA" in valor or "SANEAMIENTO" in valor:
                return "Agua y saneamiento básico"
            elif "PROPOSITO GENERAL" in valor or "PROPÓSITO GENERAL" in valor:
                 return "Inversiones con propósito general"
            elif "ASIGNACIONES ESPECIALES" in valor:
                return "Asignaciones especiales"
            else:
                return "Otras"
        ##esto junta toda la jerarquia de la base
        df_sgp_depto["texto_sgp"] = (
            df_sgp_depto["col_5"].astype(str) + " " +
            df_sgp_depto["col_6"].astype(str) + " " +
            df_sgp_depto["col_7"].astype(str) + " " +
            df_sgp_depto["col_8"].astype(str) + " " +
            df_sgp_depto["col_9"].astype(str) + " " +
            df_sgp_depto["col_10"].astype(str)
        )
        df_sgp_depto["categoria_sgp_dep"]= df_sgp_depto["texto_sgp"].apply( clasificar_cate_sgp_dep)
        df_sgp_depto=df_sgp_depto[df_sgp_depto["categoria_sgp_dep"]!= "Otras"].copy()
        ###agrupar recaudo por clasificacion
        fig_treemap_sgp_dep=px.treemap(
            df_sgp_depto,
             path=["categoria_sgp_dep","col_7"],
             values="TotalRecaudo",
        )
        #Estilo

        fig_treemap_sgp_dep.update_layout(
             margin=dict(t=40, l=10, r=10, b=10)
         )
        ##muestra porcentajes
        fig_treemap_sgp_dep.update_traces(
            textinfo="label+percent entry",
        )
        ##Texto mas estetico
        fig_treemap_sgp_dep.update_traces(
            textfont=dict(
                size=16,
                color="white"
            )
        )
        ## por ultimo un lindo borde jejejeej
        fig_treemap_sgp_dep.update_traces(
           marker=dict(
               line=dict(width=4,color="white")
           )  
        )
        st.plotly_chart(
            fig_treemap_sgp_dep,
            use_container_width=True,
             key="treemap_sgp_general_dep"
             )

        ###################################################################################################  
        ##########################MUNICIPAL##############################################################
    with tab3:
        ##Filtro de departamento
        departamentos_mun=sorted(df["Departamento"].dropna().unique())
        seleccionar_depto_mun=st.selectbox("Selecciona un Departamento", departamentos_mun ,key="mun_depto")
        df_municipios_base=df[
            (df["Departamento"]==seleccionar_depto_mun)&
            (df["Tipo de Entidad"]=="Municipio")&
            (df["Entidad"] != "Boyacá")##force a boyaca a irse jejeje
        ]
        municipios_lista=sorted(df_municipios_base["Entidad"].dropna().unique())
        ##Filtro Municipio
        seleccionar_municipio=st.selectbox("Selecciona un Municipio", municipios_lista,key="mun_entidad")
        ##data ya filtrada
        df_filtrado_m_d=df_municipios_base[df_municipios_base["Entidad"]==seleccionar_municipio]
        st.write("Cifras en miles de millones de pesos")
        col1, col2 = st.columns(2)
        with col1: 
            ##Gráfica general
            agrupar_municipios_l= df_filtrado_m_d.groupby("Año")["TotalRecaudo"].sum().reset_index()
            agrupar_municipios_l["Total_mm"]= agrupar_municipios_l["TotalRecaudo"]/1_000_000_000
            agrupar_municipios_l= agrupar_municipios_l.sort_values("Año")
            fig_gen_mun=px.line(
                agrupar_municipios_l,
                x="Año",
                y="Total_mm",
                markers=True
            )
            fig_gen_mun.update_yaxes(title=None)
            st.plotly_chart(fig_gen_mun)
            #############################################################################
        with col2:
            ##Gráfica de barras apiladas
            agrupar_mun_barrasapi=df_filtrado_m_d.groupby(["Año","clasificacion_limpia"])["TotalRecaudo"].sum().reset_index()
            agrupar_mun_barrasapi["Total_año_mun"]= agrupar_mun_barrasapi.groupby("Año")["TotalRecaudo"].transform("sum")
            agrupar_mun_barrasapi["Porcentaje_mun"]=agrupar_mun_barrasapi["TotalRecaudo"]/agrupar_mun_barrasapi["Total_año_mun"]*100
            agrupar_mun_barrasapi = agrupar_mun_barrasapi.groupby("Año").filter(
               lambda x: x["Porcentaje_mun"].sum() > 0
              )############# no deja ver años que esten en 0
            agrupar_mun_barrasapi=agrupar_mun_barrasapi.sort_values("Año")
            años_mun = sorted(agrupar_mun_barrasapi["Año"].unique())### mis años que si existen
            fig_mun_barras=px.bar(
                agrupar_mun_barrasapi,
                x="Año",
                y="Porcentaje_mun",
                color="clasificacion_limpia",
                barmode="stack"
            )
            fig_mun_barras.update_yaxes(title=None)
            fig_mun_barras.update_xaxes(
                 type="category",
                 categoryorder="array",
                 categoryarray=años_mun
                 )#################################### 
            fig_mun_barras.update_layout(legend_title=None)
            fig_mun_barras.update_layout(
               legend=dict(
                   orientation="h",
                   yanchor="top",
                   y=-0.15,
                   xanchor="left",
                   x=0
               )
            )
            st.plotly_chart( fig_mun_barras)
        #####################################FUERA COL1 Y COL 2###################################
          #Gráfica de area
        area_api_mun= df_filtrado_m_d.groupby(["Año","clas_gen"])["TotalRecaudo"].sum().reset_index()
        area_api_mun["Total_area3"]=area_api_mun.groupby("Año")["TotalRecaudo"].transform("sum")
        area_api_mun["Porcentaje_mun"]=area_api_mun["TotalRecaudo"]/ area_api_mun["Total_area3"]
        area_api_mun=area_api_mun.sort_values("Año")
        fig_area_api_mun=px.area(
            area_api_mun,
            x="Año",
            y="Porcentaje_mun",
            color="clas_gen"

        )
        fig_area_api_mun.update_yaxes(title=None)
        fig_area_api_mun.update_yaxes(tickformat=".0%")
        fig_area_api_mun.update_xaxes(
            tickmode="array",
            tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
            ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
            range=[2011.8, 2024.8]
        )
        fig_area_api_mun.update_layout(legend_title=None)
        fig_area_api_mun.update_layout(
           legend_title=None,
           legend=dict(
               orientation="h",
               yanchor="top",
               y=-0.2,
               xanchor="left",
               x=0
            )
                  
           )
        st.plotly_chart( fig_area_api_mun,use_container_width=True)    
        ############################SGP MUNICIPAL##################################
        #############################################################################
        ##Filtro de año
        año_sgp_mun=st.slider(
            "Seleccione el año",
            int(df_filtrado_m_d["Año"].min()),
            int(df_filtrado_m_d["Año"].max()),
            int(df_filtrado_m_d["Año"].max()),
            key="slider_sgp_municipal"
        )
        fil_año_mun=df_filtrado_m_d[df_filtrado_m_d["Año"]==año_sgp_mun].copy()
        df_sgp_mun=fil_año_mun[
            (
            fil_año_mun["clasificacion_ofpuj"].astype(str).str.strip().str.upper()
             == "SISTEMA GENERAL DE PARTICIPACIONES"
            )
            |
            (
            fil_año_mun["col_5"].astype(str).str.upper().str.contains(
             "PARTICIPACIONES", na=False)
            )
        ].copy()

        def clasificar_categoriaa_sgp_mun (valor):
            valor=str(valor).strip().upper()
            if "EDUCACION" in valor or "EDUCACIÓN" in valor:
                return "Educación"
            elif "SALUD" in valor:
                return "Salud"
            elif "AGUA" in valor or "SANEAMIENTO" in valor:
                return "Agua y saneamiento básico"
            elif "PROPOSITO GENERAL" in valor or "PROPÓSITO GENERAL" in valor:
                return "Inversiones con propósito general"
            elif "ASIGNACIONES ESPECIALES" in valor:
                 return "Asignaciones especiales"
            else:
                return "Otras"
        ##juntamos col de la base
        df_sgp_mun["texto_sgp_m"] = (
        df_sgp_mun["col_5"].astype(str) + " " +
        df_sgp_mun["col_6"].astype(str) + " " +
        df_sgp_mun["col_7"].astype(str) + " " +
        df_sgp_mun["col_8"].astype(str) + " " +
        df_sgp_mun["col_9"].astype(str) + " " +
        df_sgp_mun["col_10"].astype(str)
         )
        #######le aplica la clasificación a la información que unimos

        df_sgp_mun["categoria_sgp_mun"]=df_sgp_mun["texto_sgp_m"].apply(clasificar_categoriaa_sgp_mun)
        df_sgp_mun= df_sgp_mun[ df_sgp_mun["categoria_sgp_mun"]!="Otras"].copy()
        ##Gráfico
        treemap_fig_sgp_mun=px.treemap(
            df_sgp_mun,
            path=["categoria_sgp_mun","col_7"],
            values="TotalRecaudo",
            color="categoria_sgp_mun"
        )
            #Estilo

        treemap_fig_sgp_mun.update_layout(
            margin=dict(t=40, l=10, r=10, b=10)
        )
        ##muestra porcentajes
        treemap_fig_sgp_mun.update_traces(
            textinfo="label+percent entry",
        )
        ##Texto mas estetico
        treemap_fig_sgp_mun.update_traces(
            textfont=dict(
                size=16,
                color="white"
            )
        )
        ## por ultimo un lindo borde jejejeej
        treemap_fig_sgp_mun.update_traces(
           marker=dict(
               line=dict(width=4,color="white")
           )  
        )
        st.plotly_chart(
             treemap_fig_sgp_mun,
            use_container_width=True,
             key="treemap_sgp_mun"
             )

            
#Gastos    
elif  menu=="Gastos":
    st.header("Gastos")

#Coyuntura
elif  menu=="Coyuntura":
    st.header("Coyuntura")

#Treemap
elif  menu=="Treemap":
    st.header("Treemap")

#Presupuesto
elif  menu=="Presupuesto actual":
    st.header("Presupuesto actual")

#Descargas
elif  menu=="Descarga datos":
    st.header("Descarga datos")




