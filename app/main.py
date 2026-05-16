##PEPE TERRITORIAL
# Cargar librerias
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from io import BytesIO
from streamlit_option_menu import option_menu
#
st.set_page_config(layout="wide")###Que la pagina use todo el espacio
st.title("PEPE Territorial") 

menu = option_menu(
    None,
    ["Main","Ingresos","Gastos","Coyuntura","Presupuesto actual","Descarga de datos"],
    icons=[
        "house",
        "cash-coin",
        "credit-card",
        "graph-up",
        "diagram-3",
        "clipboard-data",
        "download"
    ],
    orientation="horizontal",
    default_index=0 ##donde inicia mi app(main)
)
#Que el menu cambie segun la selección
#Inicio
if menu=="Main" :
    pass
#Ingresos
elif  menu=="Ingresos":
    st.header("Ingresos")
    tab1, tab2,tab3=st.tabs(["General","Departamental","Municipal"])
    with tab1:
        #################GENERAL################################################
        ##Gráfica del historico
        st.subheader("Histórico general")
        st.caption("Cifras en miles de millones de pesos")
    #############################################################################################################
        BASE_DIR = Path(__file__).resolve().parent.parent
        df = pd.read_parquet(BASE_DIR / "data" / "ingresos_ipc_pop.parquet")
    ##############################################################################################################
    #####################################DISEÑO###############################################################
        COLORES_INGRESOS = {
       "Recursos propios": "#0FB7B3",
       "Transferencias": "#2F399B",
      "Recursos de capital": "#dd722a"
         }
    ###########################################################################################################
        ## las graficas se vean una al lado de la otra
        col1, col2=st.columns(2)
        ##agrupe los datos  por año para hacer la grafica 
        with col1:
             ##Grafica area apilada sin 100%
            ## Agrupar información
            area_df = (
            df.groupby(["Año", "clas_gen"])["TotalRecaudo_real"].sum().reset_index()
            )
            ## Pasar a miles de millones
            area_df["Total_mm"] = area_df["TotalRecaudo_real"] / 1_000_000_000
            ## Gráfica de área
            fig_area = px.area(
            area_df,
            x="Año",
            y="Total_mm",
            color="clas_gen",
            color_discrete_map=COLORES_INGRESOS
            )
            ## Ajustes visuales
            fig_area.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
            for trace in fig_area.data:
            # Convierte el color a rgba con alpha=1 (sin transparencia)
                color = trace.line.color
                trace.fillcolor = color  # usa el mismo color de la línea, sin alph
            fig_area.update_yaxes(title=None, tickformat=",.0f")
            fig_area.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )
            fig_area.update_layout(
            legend_title=None,
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="left",
            x=0
            )
            )
          
            st.plotly_chart(fig_area, use_container_width=True)
          
          ##############################################################################

        with col2:
             ##Grafica area api
            ## Agrupar información
            agrupar_barras_api_g = (
            df.groupby(["Año","clas_gen"])["TotalRecaudo_real"] .sum().reset_index() )
            agrupar_barras_api_g["Total_año"] = (
            agrupar_barras_api_g
            .groupby("Año")["TotalRecaudo_real"]
            .transform("sum")
             )

            agrupar_barras_api_g["Porcentaje"] = (
            agrupar_barras_api_g["TotalRecaudo_real"]/ agrupar_barras_api_g["Total_año"] * 100)

            fig_barras = px.bar(
            agrupar_barras_api_g,
            x="Año",
            y="Porcentaje",
            color="clas_gen",
            color_discrete_map=COLORES_INGRESOS,
            barmode="stack"
             )

            fig_barras.update_yaxes(title=None)
            fig_barras.update_layout(legend_title=None)

            fig_barras.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )

            fig_barras.update_layout(
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0
           )
           )

            st.plotly_chart(
            fig_barras,
           use_container_width=True,
           key="barras_general"
            )
            ##############################################################################
        
            #######################SGP#####################################################
            ##llamar base
##############################################################################################
            df_sgp = pd.read_parquet(BASE_DIR / "data" / "datos_sgp_pib_ic.parquet")
 ############################################################################################# 
 # ############################################################################################
 #       
        df_sgp = df_sgp[
        (df_sgp["Año"] >= 2012) &
        (df_sgp["Año"] <= 2024)
         ].copy()
        ######################################################################################
        COLORES_SGP = {
        "Agua Potable": "#F7B261",
        "Asignaciones Especiales":"#009999"  ,
        "Educación": "#dd722a",
        "Propósito General": "#0FB7B3",
        "Salud": "#2F399B"
         }    
        ##################################################################################
        st.subheader("Sistema General de Participaciones (SGP)")
        col1, col2=st.columns(2)
        with col1:
            ##Grafica area apilada sin 100%
            ## Agrupar información
            area_sgp = (
            df_sgp.groupby(["Año", "nivel_1"])["valor_constante_25"].sum().reset_index()
            )
            ## Pasar a miles de millones
            area_sgp["Total_mm"] = area_sgp["valor_constante_25"] / 1_000_000_000
            ## Gráfica de área
            fig_area_sgp = px.area(
            area_sgp,
            x="Año",
            y="Total_mm",
            color="nivel_1",
            color_discrete_map=COLORES_SGP
            )
            ## Ajustes visuales
            fig_area_sgp.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
            for trace in fig_area_sgp.data:
            # Convierte el color a rgba con alpha=1 (sin transparencia)
                color = trace.line.color
                trace.fillcolor = color  # usa el mismo color de la línea, sin alph
            fig_area_sgp .update_yaxes(title=None, tickformat=",.0f")
            fig_area_sgp .update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )
            fig_area_sgp .update_layout(
            legend_title=None,
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="left",
            x=0
            )
            )
          
            st.plotly_chart( fig_area_sgp , use_container_width=True)
          
             ############################################################################
        with col2:
           
            ##Grafica barras api
            ## Agrupar información
            agrupar_barras_api_sgp = (
            df_sgp.groupby(["Año","nivel_1"])["valor_constante_25"] .sum().reset_index() )
            agrupar_barras_api_sgp["Total_año"] = (
            agrupar_barras_api_sgp
            .groupby("Año")["valor_constante_25"]
            .transform("sum")
             )

            agrupar_barras_api_sgp["Porcentaje"] = (
            agrupar_barras_api_sgp["valor_constante_25"]/ agrupar_barras_api_sgp["Total_año"] * 100)

            fig_barras_sgp = px.bar(
            agrupar_barras_api_sgp,
            x="Año",
            y="Porcentaje",
            color="nivel_1",
            barmode="stack",
            color_discrete_map=COLORES_SGP
             )
        
            fig_barras_sgp.update_yaxes(title=None)
            fig_barras_sgp.update_layout(legend_title=None)

            fig_barras_sgp.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.5, 2025.5]
            )

            fig_barras_sgp.update_layout(
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0
           )
           )

            st.plotly_chart(
            fig_barras_sgp,
           use_container_width=True,
           key="barras_general_sgp"
            )
        #####################################################################################
         #Grafica de barras sin porcentaje
       ## SGP como porcentaje de ingresos corrientes
        ## Agrupar información
        st.subheader("Participación del SGP en los ingresos corrientes de la nación")
        barras_icn = (
            df_sgp.groupby(["Año", "nivel_1"])["valor_sgp_ingresos_corrientes"]
            .sum()
            .reset_index()
        )

        ## gráfica barras normal
        fig_barras_icn = px.bar(
            barras_icn,
            x="Año",
            y="valor_sgp_ingresos_corrientes",
            color="nivel_1",
            barmode="stack",
            color_discrete_map=COLORES_SGP
        )

        ## estética
        fig_barras_icn.update_yaxes(
            title=None
        )

        fig_barras_icn.update_layout(legend_title=None)

        fig_barras_icn.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
        )

        fig_barras_icn.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(
            fig_barras_icn,
            use_container_width=True,
            key="barras_icn_general"
        )
         
            ########################DEPARTAMENTAL#########################################
    with tab2:
        ##creo una lista de deptos
        departamentos = ["Todos"] + sorted( df["Departamento"].dropna().unique())
        ##crea mi selector
        seleccionar_depto=st.selectbox("Seleccione un Departamento",departamentos)##guarda lo que el usuario escogio
        if seleccionar_depto == "Todos":
             depto_filtrado = df.copy()
        else:
             depto_filtrado = df[df["Departamento"] == seleccionar_depto].copy()
        ###titulo
        st.caption("Cifras en miles de millones de pesos")
        col1,col2=st.columns(2)
        with col1:
           ##Gráfica general con filtro
           ##Gráfica area 
            area_df_d = (depto_filtrado.groupby(["Año", "clas_gen"])["TotalRecaudo_real"].sum().reset_index())
            ## Pasar a miles de millones
            area_df_d["Total_mm"] = area_df_d["TotalRecaudo_real"] / 1_000_000_000
            ## Gráfica de área
            fig_area_d = px.area(
            area_df_d,
            x="Año",
            y="Total_mm",
            color="clas_gen",
            color_discrete_map=COLORES_INGRESOS
            )

            ## Ajustes visuales
            fig_area_d.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
            for trace in fig_area_d.data:
            # Convierte el color a rgba con alpha=1 (sin transparencia)
                color = trace.line.color
                trace.fillcolor = color  # usa el mismo color de la línea, sin alph
            fig_area_d.update_yaxes(title=None, tickformat=",.0f")
            fig_area_d.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )
            fig_area_d.update_layout(
            legend_title=None,
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="left",
            x=0
            )
            )
          
          
            st.plotly_chart(fig_area_d, use_container_width=True,key="area_departamental")
           ######################################################################
        with col2:
            ##Gráfica barras
              ## Agrupar información
            agrupar_barras_api_d = (
            depto_filtrado.groupby(["Año","clas_gen"])["TotalRecaudo_real"] .sum().reset_index() )
            agrupar_barras_api_d["Total_año"] = (
            agrupar_barras_api_d
            .groupby("Año")["TotalRecaudo_real"]
            .transform("sum")
             )
            agrupar_barras_api_d["Porcentaje"] = (
            agrupar_barras_api_d["TotalRecaudo_real"]/ agrupar_barras_api_d["Total_año"] * 100)

            fig_barras_d = px.bar(
            agrupar_barras_api_d,
            x="Año",
            y="Porcentaje",
            color="clas_gen",
            color_discrete_map=COLORES_INGRESOS,
            barmode="stack"
             )

            fig_barras_d.update_yaxes(title=None)
            fig_barras_d.update_layout(legend_title=None)

            fig_barras_d.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )

            fig_barras_d.update_layout(
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0
           )
           )

            st.plotly_chart(
            fig_barras_d,
           use_container_width=True,
           key="barras_gene_dep_d"
            )
        ###################################################################################
            
        #########################SGP DEPARTAMENTAL#########################################
        ##################################################################################
     ############FILTRO
        if "bogot" not in seleccionar_depto.lower():
            st.subheader("Sistema General de Participaciones (SGP)")
            col1, col2 = st.columns(2)
            if seleccionar_depto == "Todos":
               df_sgp_filtrado = df_sgp.copy()
            else:
             nombre_depto_sgp = seleccionar_depto
             equivalencias_sgp = {
                "San Andrés, Providencia y Santa Catalina":
                "Archipiélago de San Andrés"
             }
             nombre_depto_sgp = equivalencias_sgp.get(
                seleccionar_depto,
                seleccionar_depto
             )

             df_sgp_filtrado = df_sgp[
                df_sgp["Nombre Departamento"]
                .str.strip()
                .str.lower()
                == nombre_depto_sgp.strip().lower()
             ].copy()
            #########################################################################################
            with col1:
                 
                 ##Gráfica area 
                 area_df_sgp= ( df_sgp_filtrado.groupby(["Año", "nivel_1"])["valor_constante_25"].sum().reset_index())
                 ## Pasar a miles de millones
                 area_df_sgp["Total_mm"] = area_df_sgp["valor_constante_25"] / 1_000_000_000
                 ## Gráfica de área
                 fig_area_sgp = px.area(
                 area_df_sgp,
                 x="Año",
                 y="Total_mm",
                 color="nivel_1",
                 color_discrete_map=COLORES_SGP
                )

                  ## Ajustes visuales
                 fig_area_sgp.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
                 for trace in  fig_area_sgp.data:
                 # Convierte el color a rgba con alpha=1 (sin transparencia)
                    color = trace.line.color
                    trace.fillcolor = color  # usa el mismo color de la línea, sin alph
                 fig_area_sgp.update_yaxes(title=None, tickformat=",.0f")
                 fig_area_sgp.update_xaxes(
                 tickmode="array",
                 tickvals=[2012,2014,2016,2018,2020,2022,2024],
                 ticktext=["2012","2014","2016","2018","2020","2022","2024"],
                 range=[2011.5, 2025.2]
                 )
                 fig_area_sgp.update_layout(
                 legend_title=None,
                 legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.15,
                 xanchor="left",
                 x=0
                 )
                 )
                 st.plotly_chart(fig_area_sgp, use_container_width=True,key="area_departamental_sgp_1")

                 
            ########################################################################################
            with col2:
                 
                 ##Grafica barras api
                ## Agrupar información
                agrupar_barras_api_ds = (
                df_sgp_filtrado.groupby(["Año","nivel_1"])["valor_constante_25"] .sum().reset_index() )
                agrupar_barras_api_ds["Total_año"] = (
                agrupar_barras_api_ds
                .groupby("Año")["valor_constante_25"]
                .transform("sum")
                 )
                agrupar_barras_api_ds["Porcentaje"] = (
                agrupar_barras_api_ds["valor_constante_25"]/ agrupar_barras_api_ds["Total_año"] * 100)
                fig_barras_ds= px.bar(
                agrupar_barras_api_ds,
                x="Año",
                y="Porcentaje",
                color="nivel_1",
                color_discrete_map=COLORES_SGP,
                barmode="stack"
                )
         
                fig_barras_ds.update_yaxes(title=None)
                fig_barras_ds.update_layout(legend_title=None)

                fig_barras_ds.update_xaxes(
                 tickmode="array",
                 tickvals=[2012,2014,2016,2018,2020,2022,2024],
                 ticktext=["2012","2014","2016","2018","2020","2022","2024"],
                 range=[2011.5, 2025.5]
                 )

                fig_barras_ds.update_layout(
                legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
                )
                )

                st.plotly_chart(
                fig_barras_ds,
                use_container_width=True,
                key="barras_general_dep_ds"
                )
            #########################################################################################
            ##Grafica barras sin porcentaje DEPTO
            st.subheader(
            f"Participación del SGP en los ingresos corrientes de la nación - {seleccionar_depto}"
            )
            barras_icd = (
                  df_sgp_filtrado.groupby(["Año", "nivel_1"])["valor_sgp_ingresos_corrientes"]
                .sum()
                .reset_index()
            )

            ## gráfica barras normal
            fig_barras_icd = px.bar(
                barras_icd,
                x="Año",
                y="valor_sgp_ingresos_corrientes",
                color="nivel_1",
                color_discrete_map=COLORES_SGP,
                barmode="stack"
            )

            ## estética
            fig_barras_icd.update_yaxes(
                title=None
            )

            fig_barras_icd.update_layout(legend_title=None)

            fig_barras_icd.update_xaxes(
                tickmode="array",
                tickvals=[2012,2014,2016,2018,2020,2022,2024],
                ticktext=["2012","2014","2016","2018","2020","2022","2024"],
                range=[2011.8, 2024.8]
            )

            fig_barras_icd.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="left",
                    x=0
                )
            )

            st.plotly_chart(
                fig_barras_icd,
                use_container_width=True,
                key="barras_icd_departamental"
            )
            
            
           
            
        ###################################################################################################  
        ##########################MUNICIPAL##############################################################
    with tab3:

        ##Filtro de departamento
        ###Crear una lista sin Bogota(MI FILL)departamentos para seleccionar
        departamentos_mun = sorted(
        df.loc[
        ~df["Departamento"].astype(str).str.strip().str.lower().str.contains("bogot", na=False),
        "Departamento"
        ].dropna().unique()
         )
        ###SELECTOR
        seleccionar_depto_mun=st.selectbox("Selecciona un Departamento", departamentos_mun ,key="mun_depto")
        ##se queda solo con el depto seleccionado y municipios (MI FILL)
        df_municipios_base = df[
         (df["Departamento"] == seleccionar_depto_mun) &
         (df["Tipo de Entidad"] == "Municipio") &
         (~df["Entidad"].astype(str).str.strip().str.lower().str.contains("bogot", na=False))
         ].copy()
        #################################################################################
        municipios_lista = ["Todos"] + sorted(df_municipios_base["Entidad"].dropna().unique())
        ##Filtro Municipio
        seleccionar_municipio=st.selectbox("Selecciona un Municipio", municipios_lista,key="mun_entidad")
        ##data ya filtrada
        if seleccionar_municipio == "Todos":
           df_filtrado_m_d = df_municipios_base.copy()
        else:
           df_filtrado_m_d = df_municipios_base[
           df_municipios_base["Entidad"] == seleccionar_municipio
           ].copy()
        st.write("Cifras en miles de millones de pesos")
        col1, col2 = st.columns(2)
        with col1: 
            ##Gráfica area
            #Gráfica de area
            area_api_mun= df_filtrado_m_d.groupby(["Año","clas_gen"])["TotalRecaudo_real"].sum().reset_index()
            area_api_mun["Total_mm"] = area_api_mun["TotalRecaudo_real"] / 1_000_000_000
            area_api_mun=area_api_mun.sort_values("Año")
            fig_area_api_mun=px.area(
             area_api_mun,
             x="Año",
             y="Total_mm",
             color="clas_gen",
             color_discrete_map=COLORES_INGRESOS
             )
            

            fig_area_api_mun.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
            for trace in fig_area_api_mun.data:
            # Convierte el color a rgba con alpha=1 (sin transparencia)
                color = trace.line.color
                trace.fillcolor = color  # usa el mismo color de la línea, sin alph
            fig_area_api_mun.update_yaxes(title=None)
            fig_area_api_mun.update_xaxes(
             tickmode="array",
             tickvals=[2012, 2014, 2016, 2018, 2020, 2022, 2024],
             ticktext=["2012", "2014", "2016", "2018", "2020", "2022", "2024"],
             range=[2011.8, 2024.8]
             )
            fig_area_api_mun.update_layout(
            legend_title=None,
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="left",
            x=0
            )
            )
            st.plotly_chart( fig_area_api_mun,use_container_width=True)  
           
            ########################################################################
            #############################################################################
        with col2:
            ##Barras api
            ## Agrupar información
            agrupar_barras_api_m = (
            df_filtrado_m_d.groupby(["Año","clas_gen"])["TotalRecaudo_real"] .sum().reset_index() )
            agrupar_barras_api_m["Total_año"] = (
            agrupar_barras_api_m
            .groupby("Año")["TotalRecaudo_real"]
            .transform("sum")
             )

            agrupar_barras_api_m["Porcentaje"] = (
            agrupar_barras_api_m["TotalRecaudo_real"]/ agrupar_barras_api_m["Total_año"] * 100)

            fig_barras_m = px.bar(
            agrupar_barras_api_m,
            x="Año",
            y="Porcentaje",
            color="clas_gen",
            color_discrete_map=COLORES_INGRESOS,
            barmode="stack"
             )

            fig_barras_m.update_yaxes(title=None)
            fig_barras_m.update_layout(legend_title=None)

            fig_barras_m.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
            )

            fig_barras_m.update_layout(
            legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="left",
            x=0
           )
           )

            st.plotly_chart(
            fig_barras_m,
           use_container_width=True,
           key="barras_gene_m"
            )
        ################################################################################ 
           
        ############################SGP MUNICIPAL##################################
        #############################################################################
        st.subheader("Sistema General de Participaciones (SGP)")
        col1, col2 = st.columns(2)
        with col1:
            ### FILTROS
            nombre_depto_sgp_m = seleccionar_depto_mun
            equivalencias_sgp = {
            "San Andrés, Providencia y Santa Catalina":
            "Archipiélago de San Andrés"
            }
            nombre_depto_sgp_m = equivalencias_sgp.get(
            seleccionar_depto_mun,
            seleccionar_depto_mun
            )
            ## SI ES TODOS LOS MUNICIPIOS
            if seleccionar_municipio == "Todos":
                df_sgp_municipio = df_sgp[
                (df_sgp["Nombre Departamento"]
                    .str.strip()
                    .str.lower()
                    == nombre_depto_sgp_m.strip().lower())
                    &
                    (df_sgp["Tipo Entidad"]
                    .str.strip()
                    .str.lower() == "municipio")
                ].copy()
            ## SI ES UN MUNICIPIO ESPECÍFICO
            else:
                df_sgp_municipio = df_sgp[
                    (df_sgp["Nombre Departamento"]
                    .str.strip()
                    .str.lower()
                    == nombre_depto_sgp_m.strip().lower())
                    &
                    (df_sgp["Nombre Entidad"]
                    .str.strip()
                    .str.lower()
                    == seleccionar_municipio.strip().lower())
                    &
                    (df_sgp["Tipo Entidad"]
                    .str.strip()
                    .str.lower() == "municipio")
                    ].copy()
        #################################################################################
        ##Graficos
        with col1:
            ##Gráfica area 
                 area_df_sgp_mun= (df_sgp_municipio.groupby(["Año", "nivel_1"])["valor_constante_25"].sum().reset_index())
                 ## Pasar a miles de millones
                 area_df_sgp_mun["Total_mm"] = area_df_sgp_mun["valor_constante_25"] / 1_000_000_000
                 ## Gráfica de área
                 fig_area_sgp_mun = px.area(
                 area_df_sgp_mun,
                 x="Año",
                 y="Total_mm",
                 color="nivel_1",
                 color_discrete_map=COLORES_SGP
                )

                  ## Ajustes visuales
                 fig_area_sgp_mun.update_traces( line=dict(width=2),selector=dict(fill='tonexty'))
                 for trace in fig_area_sgp_mun.data:
                 # Convierte el color a rgba con alpha=1 (sin transparencia)
                    color = trace.line.color
                    trace.fillcolor = color  # usa el mismo color de la línea, sin alph
                 fig_area_sgp_mun.update_yaxes(title=None, tickformat=",.0f")
                 fig_area_sgp_mun.update_xaxes(
                 tickmode="array",
                 tickvals=[2012,2014,2016,2018,2020,2022,2024],
                 ticktext=["2012","2014","2016","2018","2020","2022","2024"],
                 range=[2011.8, 2024.8]
                 )
                 fig_area_sgp_mun.update_layout(
                 legend_title=None,
                 legend=dict(
                 orientation="h",
                 yanchor="top",
                 y=-0.15,
                 xanchor="left",
                 x=0
                 )
                 )
                 st.plotly_chart(fig_area_sgp_mun, use_container_width=True,key="area_municipal_sgp")
                
            ########################################################################################
        with col2:
              ##Grafica barras api
                ## Agrupar información
                agrupar_barras_api_ms = (
                df_sgp_municipio.groupby(["Año","nivel_1"])["valor_constante_25"] .sum().reset_index() )
                agrupar_barras_api_ms["Total_año"] = (
                agrupar_barras_api_ms
                .groupby("Año")["valor_constante_25"]
                .transform("sum")
                 )
                agrupar_barras_api_ms["Porcentaje"] = (
                agrupar_barras_api_ms["valor_constante_25"]/ agrupar_barras_api_ms["Total_año"] * 100)
                fig_barras_ms= px.bar(
                agrupar_barras_api_ms,
                x="Año",
                y="Porcentaje",
                color="nivel_1",
                color_discrete_map=COLORES_SGP,
                barmode="stack"
                )

                fig_barras_ms.update_yaxes(title=None)
                fig_barras_ms.update_layout(legend_title=None)

                fig_barras_ms.update_xaxes(
                 tickmode="array",
                 tickvals=[2012,2014,2016,2018,2020,2022,2024],
                 ticktext=["2012","2014","2016","2018","2020","2022","2024"],
                 range=[2011.5, 2025.5]
                 )

                fig_barras_ms.update_layout(
                legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
                )
                )

                st.plotly_chart(
                fig_barras_ms,
                use_container_width=True,
                key="barras_general_ms_s"
                )
            ####################################################################################
        ##Grafica barras sin porcentaje
        st.subheader(
        f"Participación del SGP en los ingresos corrientes de la nación - {seleccionar_municipio}"
        )
        barras_icm = (
                   df_sgp_municipio.groupby(["Año", "nivel_1"])["valor_sgp_ingresos_corrientes"]
                .sum()
            .reset_index()
        )

        ## gráfica barras normal
        fig_barras_icm = px.bar(
            barras_icm,
            x="Año",
            y="valor_sgp_ingresos_corrientes",
            color="nivel_1",
            color_discrete_map=COLORES_SGP,
            barmode="stack"
        )

        ## estética
        fig_barras_icm.update_yaxes(
            title=None 
        )

        fig_barras_icm.update_layout(legend_title=None)

        fig_barras_icm.update_xaxes(
            tickmode="array",
            tickvals=[2012,2014,2016,2018,2020,2022,2024],
            ticktext=["2012","2014","2016","2018","2020","2022","2024"],
            range=[2011.8, 2024.8]
        )

        fig_barras_icm.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(
            fig_barras_icm,
            use_container_width=True,
            key="barras_icm_municipal"
        )
    
             
#################################################################################################################################
##########################################################################################################################################
###################################################################################################################################
#Gastos    
elif  menu=="Gastos":
    st.header("Gastos")
    ###Llamo mi Data
################################################################################################
    BASE_DIR = Path(__file__).resolve().parent.parent
    gastos_df = pd.read_parquet(BASE_DIR / "data" / "ejecucion_deflactada_mun.parquet")
 #########################################################################################
    tab1, tab2,tab3=st.tabs(["General","Departamental","Municipal"])
    with tab1:
       ##Grafico de linea  
        st.subheader("Histórico general")
        st.caption("Cifras en miles de millones de pesos")
        col1, col2=st.columns(2)
        with col1:
             ###Grafica 1
            agrupar_graf_lineagasto1=gastos_df.groupby("Año Vigencia",as_index=False)["Obligaciones_real"].sum()
            ##pasar a miles de millones
            agrupar_graf_lineagasto1["total_mm"]=agrupar_graf_lineagasto1["Obligaciones_real"]/1_000_000_000
            ##Ordenar años
            agrupar_graf_lineagasto1= agrupar_graf_lineagasto1.sort_values("Año Vigencia")
            ##Gráfica
            fig_area1_g=px.line(
                 agrupar_graf_lineagasto1,
                 x="Año Vigencia",
                 y="total_mm",
                 markers=True
            )
            ##estetica
            ## COLOR Y GROSOR
            fig_area1_g.update_traces(
                line=dict(color="#1A1F63", width=4),
                marker=dict(color="#1A1F63", size=8)
)
            fig_area1_g.update_yaxes(title=None)
            fig_area1_g.update_xaxes(title=None)
            fig_area1_g.update_xaxes(type="category"
              )
            st.plotly_chart(fig_area1_g, use_container_width=True)
         ####################################################################
        with col2:
            ###clasificación del gasto
        #######################################################################
            COLORES_GASTOS = {
            "Deuda": "#2F399B",        
            "Funcionamiento": "#0FB7B3",
            "Inversión": "#dd722a"  
             }
        #######################################################################
            gastos_df["col_2"] = gastos_df["col_2"].str.strip().str.upper()
            gastos_df["clasificacion_gastos"] = gastos_df["col_2"].replace({
            "FUNCIONAMIENTO": "Funcionamiento",
            "CONSOLIDACION": "Inversión",
            "INVERSION": "Inversión",
            "SERVICIO DE LA DEUDA PUBLICA": "Deuda"
             })
            barra_gastos_1=gastos_df.groupby(["Año Vigencia","clasificacion_gastos"], as_index=False)["Obligaciones_real"].sum()
            ###sacar total
            barra_gastos_1["total_año"]= barra_gastos_1.groupby("Año Vigencia")["Obligaciones_real"].transform("sum")
            barra_gastos_1["porcentaje"]=( barra_gastos_1["Obligaciones_real"]/ barra_gastos_1["total_año"])*100
            ##Declarar orden
            barra_gastos_1= barra_gastos_1.sort_values(["Año Vigencia", "clasificacion_gastos"])
            orden = ["Funcionamiento", "Inversión", "Deuda"]
               ##Gráfica
            fig_barras_g1=px.bar(
                  barra_gastos_1,
                  x="Año Vigencia",
                  y="porcentaje",
                  color="clasificacion_gastos",
                  color_discrete_map=COLORES_GASTOS,
                  barmode="stack",
                  category_orders={"clasificacion_gastos": orden})
            ##estetica
            fig_barras_g1.update_layout(
                legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
                )
                )
            fig_barras_g1.update_xaxes(title=None)
            fig_barras_g1.update_yaxes(title=None)
            fig_barras_g1.update_layout(legend_title=None)

            st.plotly_chart(fig_barras_g1, use_container_width=True)
            #####################################################################################
        #TREEMAP
        ## TREEMAP GENERAL GASTOS
        #############################################################
        COLORES_GASTOS_TREEMAP = {
        "FUNCIONAMIENTO": "#0FB7B3",
        "CONSOLIDACION": "#dd722a",
        "INVERSION": "#dd722a",
        "SERVICIO DE LA DEUDA PUBLICA":"#2F399B"        
}
        ############################################################
        st.subheader("Composición del gasto")
        ## filtro año
        año_treemap_g = st.slider(
            "Seleccione el año",
            min_value=2021,
            max_value=2024,
            value=2024,
            step=1,
            key="slider_treemap_gastos"
             )
        ## filtrar año
        df_treemap_g = gastos_df[
        gastos_df["Año Vigencia"] == año_treemap_g
        ].copy()
        ## pasar a miles de millones
        df_treemap_g["valor_mm"] = (
        df_treemap_g["Obligaciones_real"] / 1_000_000_000
        )
        ## treemap
        fig_treemap_g = px.treemap(
        df_treemap_g,
        path=[
            "col_2",
            "col_3",
            "col_4",
            "col_5",
            "col_6"
            ],
             values="valor_mm",
             color="col_2",
             color_discrete_map=COLORES_GASTOS_TREEMAP
             )
             ## estética
        fig_treemap_g.update_layout(
            margin=dict(t=30, l=10, r=10, b=10)
             )

        st.plotly_chart(
        fig_treemap_g,
            use_container_width=True,
            key="treemap_general_gastos_0"
            )
###################################DEPARTAMENTAL####################################################

    with tab2:
        ##arreglar nombre de san andres
        gastos_df["Departamentos"] = gastos_df["Departamento"].replace({
        "Archipiélago De San Andrés, Providencia Y Santa Catalina":
        "San Andrés, Providencia y Santa Catalina"
         })

        #crear lista de mis deptos 
        departamentos = ["Todos"] + sorted(
        gastos_df["Departamentos"].dropna().unique()
         )
        ##crear el selectbox
        seleccionar_depto = st.selectbox(
        "Seleccione un Departamento",
        departamentos,
        key="gastos_depto"
        )
        ##filtrar base
        if seleccionar_depto == "Todos":
          gastos_dep = gastos_df.copy()
        else:
          gastos_dep = gastos_df[
          gastos_df["Departamentos"] == seleccionar_depto
          ].copy()
        ##########################################################
         #grafica 1
       
        col1, col2 = st.columns(2)   
        with col1:
             agrupar_graf_lineagastod= gastos_dep.groupby("Año Vigencia",as_index=False)["Obligaciones_real"].sum()
            ##pasar a miles de millones
             agrupar_graf_lineagastod["total_mm"]=agrupar_graf_lineagastod["Obligaciones_real"]/1_000_000_000
            ##Ordenar años
             agrupar_graf_lineagastod= agrupar_graf_lineagastod.sort_values("Año Vigencia")
            ##Gráfica
             fig_area1_gd=px.line(
                 agrupar_graf_lineagastod,
                 x="Año Vigencia",
                 y="total_mm",
                 markers=True
            )
            ##estetica
             fig_area1_gd.update_traces(
                line=dict(color="#1A1F63", width=4),
                marker=dict(color="#1A1F63", size=8))
             fig_area1_gd.update_yaxes(title=None)
             fig_area1_gd.update_xaxes(title=None)
             fig_area1_gd.update_xaxes(type="category"
              )
             st.plotly_chart(fig_area1_gd, use_container_width=True,key="area_gastos_departamental")
            #########################################################
            # 2 grafica
        with col2:
            
             gastos_dep["col_2"] = gastos_dep["col_2"].str.strip().str.upper()
             gastos_dep["clasificacion_gastos"] = gastos_dep["col_2"].replace({
            "FUNCIONAMIENTO": "Funcionamiento",
            "CONSOLIDACION": "Inversión",
            "INVERSION": "Inversión",
            "SERVICIO DE LA DEUDA PUBLICA": "Deuda"
             })
             barra_gastos_d=gastos_dep.groupby(["Año Vigencia","clasificacion_gastos"], as_index=False)["Obligaciones_real"].sum()
            ###sacar total
             barra_gastos_d["total_año"]= barra_gastos_d.groupby("Año Vigencia")["Obligaciones_real"].transform("sum")
             barra_gastos_d["porcentaje"]=( barra_gastos_d["Obligaciones_real"]/ barra_gastos_d["total_año"])*100
            ##Declarar orden
             barra_gastos_d= barra_gastos_d.sort_values(["Año Vigencia", "clasificacion_gastos"])
             orden = ["Funcionamiento", "Inversión", "Deuda"]
               ##Gráfica
             fig_barras_gd=px.bar(
                  barra_gastos_d,
                  x="Año Vigencia",
                  y="porcentaje",
                  color="clasificacion_gastos",
                  color_discrete_map=COLORES_GASTOS,
                  barmode="stack",
                  category_orders={"clasificacion_gastos": orden})
            ##estetica
             fig_barras_gd.update_layout(
                legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="left",
                x=0
                )
                )
             fig_barras_gd.update_xaxes(title=None)
             fig_barras_gd.update_yaxes(title=None)
             fig_barras_gd.update_layout(legend_title=None)

             st.plotly_chart(fig_barras_gd, use_container_width=True, key="barras_gastos_departamental")
            ########################################################################
        #TREEMAP DEPTO
        ## TREEMAP GENERAL GASTOS
        st.subheader("Composición del gasto")
        ## filtro año
        año_treemap_gd = st.slider(
            "Seleccione el año",
            min_value=2021,
            max_value=2024,
            value=2024,
            step=1,
            key="slider_treemap_gastos_d"
             )
        ## filtrar año
        df_treemap_gd =  gastos_dep[
        gastos_dep["Año Vigencia"] == año_treemap_gd
        ].copy()
        ## pasar a miles de millones
        df_treemap_gd["valor_mm"] = (
        df_treemap_gd["Obligaciones_real"] / 1_000_000_000
        )
        ## treemap
        fig_treemap_gd = px.treemap(
        df_treemap_gd,
        path=[
            "col_2",
            "col_3",
            "col_4",
            "col_5",
            "col_6"
            ],
             values="valor_mm",
             color="col_2",
             color_discrete_map=COLORES_GASTOS_TREEMAP
             )
             ## estética
        fig_treemap_gd.update_layout(
            margin=dict(t=30, l=10, r=10, b=10)
             )

        st.plotly_chart(
        fig_treemap_gd,
            use_container_width=True,
            key="treemap_general_gastos_1"
            )


            
        

##############################MUNICIPAL##################################################
    with tab3:
               #####################################################################
            ## LISTA DE DEPARTAMENTOS
            #####################################################################

            departamentos = ["Todos"] + sorted(
                gastos_df.loc[
                    gastos_df["Tipo de Entidad"] == "Departamento",
                    "Departamento"
                ].dropna().unique()
            )

            seleccionar_depto_mun = st.selectbox(
                "Seleccione un Departamento",
                departamentos,
                key="gastos_depto_a"
            )

            #####################################################################
            ## BASE MUNICIPIOS
            #####################################################################

            if seleccionar_depto_mun == "Todos":

                gastos_mun_base = gastos_df[
                    gastos_df["Tipo de Entidad"] == "Municipio"
                ].copy()

            else:

                ## sacar codigo del departamento
                codigo_depto = (
                    gastos_df.loc[
                        (gastos_df["Tipo de Entidad"] == "Departamento") &
                        (gastos_df["Departamento"] == seleccionar_depto_mun),
                        "Código DANE"
                    ]
                    .astype(str)
                    .str.zfill(5)
                    .str[:2]
                    .iloc[0]
                )

                ## municipios de ese departamento
                gastos_mun_base = gastos_df[
                    (gastos_df["Tipo de Entidad"] == "Municipio") &
                    (
                        gastos_df["Código DANE"]
                        .astype(str)
                        .str.zfill(5)
                        .str[:2]
                        == codigo_depto
                    )
                ].copy()

            #####################################################################
            ## LISTA MUNICIPIOS
            #####################################################################

            municipios = ["Todos"] + sorted(
                gastos_mun_base["Nombre_Mun"].dropna().unique()
            )

            seleccionar_municipio_g = st.selectbox(
                "Seleccione un Municipio",
                municipios,
                key="gastos_municipio"
            )

            #####################################################################
            ## FILTRO FINAL
            #####################################################################

            if seleccionar_municipio_g == "Todos":

                gastos_mun = gastos_mun_base.copy()

            else:

                gastos_mun = gastos_mun_base[
                    gastos_mun_base["Nombre_Mun"] == seleccionar_municipio_g
                ].copy()
        #########################################################################################################
         ##########################################################
         #grafica 1 
            col1, col2 = st.columns(2)   
            with col1:
                agrupar_graf_lineagastom= gastos_mun.groupby("Año Vigencia",as_index=False)["Obligaciones_real"].sum()
                ##pasar a miles de millones
                agrupar_graf_lineagastom["total_mm"]=agrupar_graf_lineagastom["Obligaciones_real"]/1_000_000_000
                ##Ordenar años
                agrupar_graf_lineagastom= agrupar_graf_lineagastom.sort_values("Año Vigencia")
                ##Gráfica
                fig_area1_gm=px.line(
                    agrupar_graf_lineagastom,
                    x="Año Vigencia",
                    y="total_mm",
                    markers=True
                )
                ##estetica
                fig_area1_gm.update_traces(
                line=dict(color="#1A1F63", width=4),
                marker=dict(color="#1A1F63", size=8))
                fig_area1_gm.update_yaxes(title=None)
                fig_area1_gm.update_xaxes(title=None)
                fig_area1_gm.update_xaxes(type="category"
                )
                st.plotly_chart(fig_area1_gm, use_container_width=True,key="area_gastos_municipal")
            #########################################################
            # 2 grafica
            with col2:
                gastos_mun["col_2"] = gastos_mun["col_2"].str.strip().str.upper()
                gastos_mun["clasificacion_gastos"] = gastos_mun["col_2"].replace({
                "FUNCIONAMIENTO": "Funcionamiento",
                "CONSOLIDACION": "Inversión",
                "INVERSION": "Inversión",
                "SERVICIO DE LA DEUDA PUBLICA": "Deuda"
                })
                barra_gastos_m=gastos_mun.groupby(["Año Vigencia","clasificacion_gastos"], as_index=False)["Obligaciones_real"].sum()
                ###sacar total
                barra_gastos_m["total_año"]= barra_gastos_m.groupby("Año Vigencia")["Obligaciones_real"].transform("sum")
                barra_gastos_m["porcentaje"]=( barra_gastos_m["Obligaciones_real"]/ barra_gastos_m["total_año"])*100
                ##Declarar orden
                barra_gastos_m= barra_gastos_m.sort_values(["Año Vigencia", "clasificacion_gastos"])
                orden = ["Funcionamiento", "Inversión", "Deuda"]
                ##Gráfica
                fig_barras_gm=px.bar(
                    barra_gastos_m,
                    x="Año Vigencia",
                    y="porcentaje",
                    color="clasificacion_gastos",
                    color_discrete_map=COLORES_GASTOS,
                    barmode="stack",
                    category_orders={"clasificacion_gastos": orden})
                ##estetica
                fig_barras_gm.update_layout(
                    legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.2,
                    xanchor="left",
                    x=0
                    )
                    )
                fig_barras_gm.update_xaxes(title=None)
                fig_barras_gm.update_yaxes(title=None)
                fig_barras_gm.update_layout(legend_title=None)

                st.plotly_chart(fig_barras_gm, use_container_width=True, key="barras_gastos_municipal")
            ########################################################################
            #TREEMAP MUN
            ## TREEMAP GENERAL GASTOS
            st.subheader("Composición del gasto")
            ## filtro año
            año_treemap_gm = st.slider(
                "Seleccione el año",
                min_value=2021,
                max_value=2024,
                value=2024,
                step=1,
                key="slider_treemap_gastos_m"
                )
            ## filtrar año
            df_treemap_gm =  gastos_mun[
            gastos_mun["Año Vigencia"] == año_treemap_gm
            ].copy()
            ## pasar a miles de millones
            df_treemap_gm["valor_mm"] = (
            df_treemap_gm["Obligaciones_real"] / 1_000_000_000
            )
            ## treemap
            fig_treemap_gm = px.treemap(
            df_treemap_gm,
            path=[
                "col_2",
                "col_3",
                "col_4",
                "col_5",
                "col_6"
                ],
                values="valor_mm",
                color="col_2",
                color_discrete_map=COLORES_GASTOS_TREEMAP

                )
                ## estética
            fig_treemap_gm.update_layout(
                margin=dict(t=30, l=10, r=10, b=10)
                )

            st.plotly_chart(
            fig_treemap_gm,
                use_container_width=True,
                key="treemap_general_gastos_mun"
                )
######################################################################################################            
elif menu == "Coyuntura":
    st.header("Coyuntura - Ejecución de Ingresos 2025")
  
    

    import os
    from pathlib import Path
    import plotly.graph_objects as go


    ejec_path = r"C:\PEPE_TERRITORIAL\data\eje_ing_clean25.xlsx"
    prog_path = r"C:\PEPE_TERRITORIAL\data\pro_ing_clean25.xlsx" 

    @st.cache_data
    def cargar_datos(ejec_path, prog_path):
        df_ejec = pd.read_excel(ejec_path)
        df_prog = pd.read_excel(prog_path)
        return df_ejec, df_prog

    df_ejec, df_prog = cargar_datos(ejec_path, prog_path)
    ###########################################################################################################

   
    st.header("Coyuntura - Ejecución Presupuestal Territorial")

    DATOS_LISTOS = False  # ← cambiar a True cuando el CIFFIT actualice

    if not DATOS_LISTOS:
        st.info(" Esperando actualización del CIFFIT.")
    else:

        tab_ing, tab_gas = st.tabs(["Ingresos 2025", "Gastos 2025"])

        # =========================================================================
        # HELPERS COMPARTIDOS
        # =========================================================================
        def fmt_cop(n):
            if n >= 1e12: return f"${n/1e12:.2f} B"
            if n >= 1e9:  return f"${n/1e9:.1f} MM"
            return f"${n/1e6:.0f} M"

        def tarjeta_metrica(label, valor_cop, color_valor):
            return f"""
            <div style="background:#F1EFE8; border-radius:12px; padding:14px 18px;
                        margin-bottom:10px; border-left:4px solid {color_valor};">
                <div style="font-size:11px; font-weight:600; color:#888780;
                            letter-spacing:.06em; text-transform:uppercase;
                            margin-bottom:4px;">{label}</div>
                <div style="font-size:22px; font-weight:600; color:{color_valor};
                            font-family:'Inter',sans-serif;">{valor_cop}</div>
            </div>
            """

        # Paleta de colores por clasificación e impuesto
        COLOR_CLAS = {
            "Recursos propios":    "#185FA5",
            "Transferencias":      "#0F6E56",
            "Recursos de capital": "#BA7517",
        }
        COLOR_IMP = {
            "Estampillas":                          "#534AB7",
            "Sobretasa a la gasolina":              "#0F6E56",
            "Impuesto predial unificado":           "#185FA5",
            "Impuesto de industria y comercio":     "#BA7517",
        }

        # -------------------------------------------------------------------------
        # Función reutilizable: gauge limpio sin fondo blanco
        # -------------------------------------------------------------------------
        def make_gauge(value, title_text, subtitle="", color="#185FA5",
                    height=280, font_size=52, show_threshold=False, threshold_val=58.3):
            steps  = [
                {"range": [0,  40], "color": "#FCEBEB"},
                {"range": [40, 70], "color": "#FAEEDA"},
                {"range": [70,100], "color": "#EAF3DE"},
            ]
            gauge_cfg = {
                "axis":        {"range": [0, 100], "tickwidth": 1,
                                "tickcolor": "#888780", "tickfont": {"size": 11}, "dtick": 20},
                "bar":         {"color": color, "thickness": 0.28},
                "bgcolor":     "rgba(0,0,0,0)",   # fondo interno transparente
                "borderwidth": 0,
                "steps":       steps,
            }
            if show_threshold:
                gauge_cfg["threshold"] = {
                    "line": {"color": "#D85A30", "width": 3},
                    "thickness": 0.85,
                    "value": threshold_val,
                }
            full_title = (
                f"{title_text}<br>"
                f"<span style='font-size:13px;color:#888780'>{subtitle}</span>"
                if subtitle else title_text
            )
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number={"suffix": "%", "font": {"size": font_size, "color": "#1a1a2e",
                                                "family": "Inter, sans-serif"}},
                gauge=gauge_cfg,
                title={"text": full_title,
                    "font": {"size": 17, "color": "#1a1a2e", "family": "Inter, sans-serif"}},
            ))
            fig.update_layout(
                height=height,
                margin=dict(t=60, b=10, l=20, r=20),
                paper_bgcolor="rgba(0,0,0,0)",   # ← sin fondo blanco
                plot_bgcolor ="rgba(0,0,0,0)",
                font_family="Inter, sans-serif",
            )
            return fig

        # =========================================================================
        # TAB INGRESOS 2025
        # =========================================================================
        with tab_ing:

            # ----- Carga de datos ------------------------------------------------
            base_dir  = Path(__file__).parent
            ejec_path = base_dir / "eje_ing_clean25.xlsx"
            prog_path = base_dir / "pro_ing_clean25.xlsx"

            @st.cache_data
            def cargar_ingresos():
                df_e = pd.read_excel(ejec_path)
                df_p = pd.read_excel(prog_path)
                for df in [df_e, df_p]:
                    df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                    df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                    df["Departamento"]    = df["Departamento"].astype(str).str.strip()
                return df_e, df_p

            df_ejec, df_prog = cargar_ingresos()

            # ----- Consolidado por entidad ---------------------------------------
            group_cols = ["Entidad", "Tipo de Entidad", "Departamento"]

            ejec_agg = (df_ejec.groupby(group_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_agg = (df_prog.groupby(group_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))

            tabla = pd.merge(prog_agg, ejec_agg, on=group_cols, how="left")
            tabla["Total_Ejecutado"]   = tabla["Total_Ejecutado"].fillna(0)
            tabla["Tasa_Ejecución (%)"]= ((tabla["Total_Ejecutado"] / tabla["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Consolidado por clas_gen2 (clasificación) --------------------
            det_cols = group_cols + ["clas_gen2"]
            ejec_det = (df_ejec.groupby(det_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_det = (df_prog.groupby(det_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))
            detalle  = pd.merge(prog_det, ejec_det, on=det_cols, how="left")
            detalle["Total_Ejecutado"]    = detalle["Total_Ejecutado"].fillna(0)
            detalle["Tasa_Ejecución (%)"] = ((detalle["Total_Ejecutado"] / detalle["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Consolidado por clas_ofpuj (impuestos) -----------------------
            ofp_cols = group_cols + ["clas_ofpuj"]
            ejec_ofp = (df_ejec.groupby(ofp_cols, as_index=False)["Total Recaudo"]
                            .sum().rename(columns={"Total Recaudo": "Total_Ejecutado"}))
            prog_ofp = (df_prog.groupby(ofp_cols, as_index=False)["Presupuesto Definitivo"]
                            .sum().rename(columns={"Presupuesto Definitivo": "Total_Programado"}))
            ofpuj    = pd.merge(prog_ofp, ejec_ofp, on=ofp_cols, how="left")
            ofpuj["Total_Ejecutado"]    = ofpuj["Total_Ejecutado"].fillna(0)
            ofpuj["Tasa_Ejecución (%)"] = ((ofpuj["Total_Ejecutado"] / ofpuj["Total_Programado"]) * 100).round(2).fillna(0)

            # ----- Totales generales --------------------------------------------
            def tasas(df_sub):
                p = df_sub["Total_Programado"].sum()
                e = df_sub["Total_Ejecutado"].sum()
                t = round(e / p * 100, 2) if p > 0 else 0
                return p, e, t

            p_gen,  e_gen,  t_gen  = tasas(tabla)
            p_dep,  e_dep,  t_dep  = tasas(tabla[tabla["Tipo de Entidad"] == "Departamento"])
            p_mun,  e_mun,  t_mun  = tasas(tabla[tabla["Tipo de Entidad"] == "Municipio"])

            # =====================================================================
            # PESTAÑAS INGRESOS
            # =====================================================================
            tab1, tab2, tab3 = st.tabs(["General", "Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # TAB 1 – GENERAL
            # ------------------------------------------------------------------
            with tab1:
                st.subheader("Ejecución Acumulada General")
                col1, col2, col3 = st.columns(3)

                for col, tasa, prog, ejec, titulo in [
                    (col1, t_gen,  p_gen,  e_gen,  "Nacional"),
                    (col2, t_dep,  p_dep,  e_dep,  "Departamentos"),
                    (col3, t_mun,  p_mun,  e_mun,  "Municipios"),
                ]:
                    with col:
                        st.plotly_chart(
                            make_gauge(tasa, titulo, show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption(f"**Ejecutado / Programado:** {fmt_cop(ejec)} / {fmt_cop(prog)}")
                        st.divider()
                        if tasa > 100:
                            st.metric("Sobreejecución", f"+{tasa-100:.1f}%",
                                    f"+{fmt_cop(ejec-prog)}", delta_color="normal")
                        else:
                            st.metric("Falta por ejecutar", f"{100-tasa:.1f}%",
                                    f"{fmt_cop(prog-ejec)} restantes", delta_color="inverse")

            # ------------------------------------------------------------------
            # TAB 2 – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with tab2:
                st.subheader("Nivel Departamental")
                df_dep = tabla[tabla["Tipo de Entidad"] == "Departamento"].copy()

                if df_dep.empty:
                    st.info("No hay datos departamentales disponibles.")
                else:
                    entidad_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_dep["Entidad"].unique()),
                        key="ing_dep_sel",
                    )
                    row    = df_dep[df_dep["Entidad"] == entidad_sel].iloc[0]
                    tasa   = row["Tasa_Ejecución (%)"]
                    prog   = row["Total_Programado"]
                    ejec   = row["Total_Ejecutado"]

                    # — Gauge principal + métricas —
                    col_gauge, col_metrics = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(tasa, "Tasa de ejecución total",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}",
                                    show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption("**Ejecutado / Programado**")

                    with col_metrics:
                        st.markdown(tarjeta_metrica("Programado",  fmt_cop(prog),        "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado",   fmt_cop(ejec),        "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Rezago",      fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)

                    st.divider()

                    # — Zona 2: Clasificación | Impuesto —
                    col_clas, col_imp = st.columns(2)

                    # ── Clasificación clas_gen2 (gauge individual) ──────────────
                    with col_clas:
                        st.markdown("### Ejecución por Clasificación")
                        opciones_clas = ["Recursos propios", "Transferencias", "Recursos de capital"]
                        clas_sel = st.selectbox(
                            "Selecciona una clasificación",
                            opciones_clas,
                            key="ing_clas_dep",
                        )
                        df_c = detalle[
                            (detalle["Entidad"] == entidad_sel) &
                            (detalle["clas_gen2"] == clas_sel)
                        ]
                        if not df_c.empty:
                            p_c = df_c["Total_Programado"].sum()
                            e_c = df_c["Total_Ejecutado"].sum()
                            t_c = round(e_c / p_c * 100, 2) if p_c > 0 else 0
                            color_c = COLOR_CLAS.get(clas_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_c, clas_sel, color=color_c, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_c)}** / Programado: **{fmt_cop(p_c)}**")
                        else:
                            st.info(f"Sin datos para {clas_sel}.")

                    # ── Impuesto principal (gauge individual) ──────────────────
                    with col_imp:
                        st.markdown("### Impuestos Principales")
                        opciones_imp_dep = ["Estampillas", "Sobretasa a la gasolina"]
                        imp_sel = st.selectbox(
                            "Selecciona un impuesto",
                            opciones_imp_dep,
                            key="ing_imp_dep",
                        )
                        mask   = ofpuj["clas_ofpuj"].str.contains(imp_sel, case=False, na=False)
                        df_imp = ofpuj[(ofpuj["Entidad"] == entidad_sel) & mask]
                        if not df_imp.empty:
                            p_i = df_imp["Total_Programado"].sum()
                            e_i = df_imp["Total_Ejecutado"].sum()
                            t_i = round(e_i / p_i * 100, 2) if p_i > 0 else 0
                            color_i = COLOR_IMP.get(imp_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_i, imp_sel, color=color_i, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_i)}** / Programado: **{fmt_cop(p_i)}**")
                        else:
                            st.info(f"Sin datos para {imp_sel}.")

                    st.divider()
                    with st.expander("Ver tabla de detalle completa"):
                        st.dataframe(tabla[tabla["Entidad"] == entidad_sel], use_container_width=True)

            # ------------------------------------------------------------------
            # TAB 3 – MUNICIPAL
            # ------------------------------------------------------------------
            with tab3:
                st.subheader("Nivel Municipal")
                df_mun_t = tabla[tabla["Tipo de Entidad"] == "Municipio"].copy()

                if df_mun_t.empty:
                    st.info("No hay datos municipales disponibles.")
                else:
                    deptos_mun = sorted(df_mun_t["Departamento"].unique())
                    depto_sel  = st.selectbox("Selecciona un Departamento", deptos_mun, key="ing_mun_depto_sel")
                    muns_lista = sorted(df_mun_t[df_mun_t["Departamento"] == depto_sel]["Entidad"].unique())
                    entidad_sel = st.selectbox("Selecciona un Municipio", muns_lista, key="ing_mun_sel")

                    row  = df_mun_t[df_mun_t["Entidad"] == entidad_sel].iloc[0]
                    tasa = row["Tasa_Ejecución (%)"]
                    prog = row["Total_Programado"]
                    ejec = row["Total_Ejecutado"]

                    # — Gauge principal + métricas —
                    col_gauge, col_metrics = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(tasa, "Tasa de ejecución total",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}",
                                    show_threshold=True),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption("**Ejecutado / Programado**")

                    with col_metrics:
                        st.markdown(tarjeta_metrica("Programado",  fmt_cop(prog),        "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado",   fmt_cop(ejec),        "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Rezago",      fmt_cop(prog - ejec), "#D85A30"), unsafe_allow_html=True)

                    st.divider()

                    # — Zona 2: Clasificación | Impuesto —
                    col_clas, col_imp = st.columns(2)

                    # ── Clasificación clas_gen2 (gauge individual) ──────────────
                    with col_clas:
                        st.markdown("### Ejecución por Clasificación")
                        opciones_clas = ["Recursos propios", "Transferencias", "Recursos de capital"]
                        clas_sel = st.selectbox(
                            "Selecciona una clasificación",
                            opciones_clas,
                            key="ing_clas_mun",
                        )
                        df_c = detalle[
                            (detalle["Entidad"] == entidad_sel) &
                            (detalle["clas_gen2"] == clas_sel)
                        ]
                        if not df_c.empty:
                            p_c = df_c["Total_Programado"].sum()
                            e_c = df_c["Total_Ejecutado"].sum()
                            t_c = round(e_c / p_c * 100, 2) if p_c > 0 else 0
                            color_c = COLOR_CLAS.get(clas_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_c, clas_sel, color=color_c, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_c)}** / Programado: **{fmt_cop(p_c)}**")
                        else:
                            st.info(f"Sin datos para {clas_sel}.")

                    # ── Impuesto principal (gauge individual) ──────────────────
                    with col_imp:
                        st.markdown("### Impuestos Principales")
                        opciones_imp_mun = [
                            "Impuesto predial unificado",
                            "Impuesto de industria y comercio",
                            "Sobretasa a la gasolina",
                            "Estampillas",
                        ]
                        imp_sel = st.selectbox(
                            "Selecciona un impuesto",
                            opciones_imp_mun,
                            key="ing_imp_mun",
                        )
                        # Máscara flexible según el impuesto
                        if "predial" in imp_sel.lower():
                            mask = ofpuj["clas_ofpuj"].str.contains("predial", case=False, na=False)
                        elif "industria" in imp_sel.lower() or "comercio" in imp_sel.lower():
                            mask = ofpuj["clas_ofpuj"].str.contains("industria|comercio|ICA", case=False, na=False)
                        else:
                            mask = ofpuj["clas_ofpuj"].str.contains(imp_sel, case=False, na=False)

                        df_imp = ofpuj[(ofpuj["Entidad"] == entidad_sel) & mask]
                        if not df_imp.empty:
                            p_i = df_imp["Total_Programado"].sum()
                            e_i = df_imp["Total_Ejecutado"].sum()
                            t_i = round(e_i / p_i * 100, 2) if p_i > 0 else 0
                            color_i = COLOR_IMP.get(imp_sel, "#185FA5")
                            st.plotly_chart(
                                make_gauge(t_i, imp_sel, color=color_i, height=240, font_size=40),
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.caption(f"Ejecutado: **{fmt_cop(e_i)}** / Programado: **{fmt_cop(p_i)}**")
                        else:
                            st.info(f"Sin datos para {imp_sel}.")

                    st.divider()
                    with st.expander("Ver tabla de detalle completa"):
                        st.dataframe(tabla[tabla["Entidad"] == entidad_sel], use_container_width=True)

        # =========================================================================
        # TAB GASTOS 2025
        # =========================================================================
        with tab_gas:
            st.header("Coyuntura de Gastos 2025")
        
            base_dir  = Path(__file__).parent
            ejec_path = base_dir / "eje_gast_clean25.xlsx"
            prog_path = base_dir / "pro_gast_clean25.xlsx"

            @st.cache_data
            def cargar_gastos():
                df_eg = pd.read_excel(ejec_path)
                df_pg = pd.read_excel(prog_path)
                for df in [df_eg, df_pg]:
                    df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                    df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                    df["Departamento"]    = df["Departamento"].astype(str).str.strip()
                return df_eg, df_pg

            df_ejec_g, df_prog_g = cargar_gastos()

            group_cols = ["Entidad", "Tipo de Entidad", "Departamento"]
            ejec_agg_g = (df_ejec_g.groupby(group_cols, as_index=False)["Obligaciones"]
                                .sum().rename(columns={"Obligaciones": "Total_Ejecutado"}))
            prog_agg_g = (df_prog_g.groupby(group_cols, as_index=False)["Apropiación Definitiva"]
                                .sum().rename(columns={"Apropiación Definitiva": "Total_Programado"}))
            tabla_g = pd.merge(prog_agg_g, ejec_agg_g, on=group_cols, how="left")
            tabla_g["Total_Ejecutado"]    = tabla_g["Total_Ejecutado"].fillna(0)
            tabla_g["Tasa_Ejecución (%)"] = ((tabla_g["Total_Ejecutado"] / tabla_g["Total_Programado"]) * 100).round(2).fillna(0)

            p_gen_g, e_gen_g, t_gen_g = tasas(tabla_g)
            p_dep_g, e_dep_g, t_dep_g = tasas(tabla_g[tabla_g["Tipo de Entidad"] == "Departamento"])
            p_mun_g, e_mun_g, t_mun_g = tasas(tabla_g[tabla_g["Tipo de Entidad"] == "Municipio"])

            tab1g, tab2g, tab3g = st.tabs(["General", "Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # GASTOS – TAB GENERAL
            # ------------------------------------------------------------------
            with tab1g:
                st.subheader("Ejecución Acumulada General de Gastos")
                col1, col2, col3 = st.columns(3)
                for col, tasa, prog, ejec, titulo in [
                    (col1, t_gen_g, p_gen_g, e_gen_g, "Nacional"),
                    (col2, t_dep_g, p_dep_g, e_dep_g, "Departamentos"),
                    (col3, t_mun_g, p_mun_g, e_mun_g, "Municipios"),
                ]:
                    with col:
                        st.plotly_chart(
                            make_gauge(tasa, titulo),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                        st.caption(f"**Obligaciones / Apropiación:** {fmt_cop(ejec)} / {fmt_cop(prog)}")

            # ------------------------------------------------------------------
            # GASTOS – TAB DEPARTAMENTAL
            # ------------------------------------------------------------------
            with tab2g:
                st.subheader("Nivel Departamental")
                df_dep_g = tabla_g[tabla_g["Tipo de Entidad"] == "Departamento"].copy()
                if not df_dep_g.empty:
                    entidad_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_dep_g["Entidad"].unique()),
                        key="gasto_dep_sel",
                    )
                    row = df_dep_g[df_dep_g["Entidad"] == entidad_sel].iloc[0]
                    col_gauge, col_info = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(row["Tasa_Ejecución (%)"],
                                    "Tasa de ejecución",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}"),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    with col_info:
                        st.markdown(tarjeta_metrica("Programado",           fmt_cop(row["Total_Programado"]),                     "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado (Obl.)",     fmt_cop(row["Total_Ejecutado"]),                      "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Por Ejecutar",         fmt_cop(row["Total_Programado"] - row["Total_Ejecutado"]), "#D85A30"), unsafe_allow_html=True)

            # ------------------------------------------------------------------
            # GASTOS – TAB MUNICIPAL
            # ------------------------------------------------------------------
            with tab3g:
                st.subheader("Nivel Municipal")
                df_mun_g = tabla_g[tabla_g["Tipo de Entidad"] == "Municipio"].copy()
                if not df_mun_g.empty:
                    depto_sel = st.selectbox(
                        "Selecciona Departamento",
                        sorted(df_mun_g["Departamento"].unique()),
                        key="gasto_mun_depto",
                    )
                    muns_g    = sorted(df_mun_g[df_mun_g["Departamento"] == depto_sel]["Entidad"].unique())
                    entidad_sel = st.selectbox("Selecciona Municipio", muns_g, key="gasto_mun_sel")
                    row = df_mun_g[df_mun_g["Entidad"] == entidad_sel].iloc[0]
                    col_gauge, col_info = st.columns([1.4, 1])
                    with col_gauge:
                        st.plotly_chart(
                            make_gauge(row["Tasa_Ejecución (%)"],
                                    "Tasa de ejecución",
                                    subtitle=f"Acumulado 2025 · {entidad_sel}"),
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    with col_info:
                        st.markdown(tarjeta_metrica("Programado",       fmt_cop(row["Total_Programado"]),                     "#185FA5"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Ejecutado (Obl.)", fmt_cop(row["Total_Ejecutado"]),                      "#1D9E75"), unsafe_allow_html=True)
                        st.markdown(tarjeta_metrica("Por Ejecutar",     fmt_cop(row["Total_Programado"] - row["Total_Ejecutado"]), "#D85A30"), unsafe_allow_html=True)
        
    
        #################################################################################################################
        ################################################################################################################

#Presupuesto
elif  menu=="Presupuesto actual":
    ##Cargar base
     st.header("Presupuesto actual 2025")

    # -------------------------------------------------------------------------
    # Carga de datos
    # -------------------------------------------------------------------------
     DATOS_LISTOS = False  # ← cambiar a True cuando el CIFFIT actualice

     if not DATOS_LISTOS:
        st.info(" Esperando actualización del CIFFIT.")
     else:
        base_dir  = Path(__file__).parent

        @st.cache_data
        def cargar_presupuesto():
            df_ing  = pd.read_excel(base_dir / "pro_ing_clean25.xlsx")
            df_gast = pd.read_excel(base_dir / "pro_gast_clean25.xlsx")

            for df in [df_ing, df_gast]:
                df["Entidad"]         = df["Entidad"].astype(str).str.strip()
                df["Tipo de Entidad"] = df["Tipo de Entidad"].astype(str).str.strip()
                df["Departamento"]    = df["Departamento"].astype(str).str.strip()

            return df_ing, df_gast

        df_ing, df_gast = cargar_presupuesto()

        # -------------------------------------------------------------------------
        # Helpers
        # -------------------------------------------------------------------------
        def fmt_cop(n):
            """Formato COP legible."""
            if n >= 1e12: return f"${n/1e12:.2f} B"
            if n >= 1e9:  return f"${n/1e9:.1f} MM"
            return f"${n/1e6:.0f} M"

        def limpiar_path(df, cols):
            """
            Para treemaps: propaga hacia adelante los valores de la jerarquía
            y descarta filas completamente vacías en la primera columna del path.
            """
            df = df.copy()
            df[cols[0]] = df[cols[0]].fillna("Sin clasificar")
            for i in range(1, len(cols)):
                df[cols[i]] = df[cols[i]].fillna(df[cols[i - 1]])
            return df

        def estilo_treemap(fig):
            """Estética uniforme para todos los treemaps."""
            fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
            fig.update_traces(
                textinfo="label+percent entry",
                textfont=dict(size=14, color="white"),
                marker=dict(line=dict(width=3, color="white")),
            )
            return fig

        def metrica_total(df, col_valor, label):
            total = df[col_valor].sum()
            st.metric(label, fmt_cop(total))

        # =========================================================================
        # TABS PRINCIPALES: Ingresos | Gastos
        # =========================================================================
        tab_ing_p, tab_gast_p = st.tabs([" Ingresos 2025", "Gastos 2025"])

        # =========================================================================
        # INGRESOS 2025
        # =========================================================================
        with tab_ing_p:
            st.subheader("Programación de Ingresos 2025")

            PATH_ING  = ["clas_ofpuj", "clas_gen1", "clas_gen2"]
            COL_VAL_I = "Presupuesto Definitivo"

            # Limpiar columnas de path
            df_ing_clean = limpiar_path(df_ing, PATH_ING)
            df_ing_clean["valor_mm"] = df_ing_clean[COL_VAL_I] / 1_000_000_000

            # Sub-tabs territoriales
            t_dep_i, t_mun_i = st.tabs(["Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # INGRESOS – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with t_dep_i:
                df_dep_i = df_ing_clean[
                    df_ing_clean["Tipo de Entidad"] == "Departamento"
                ].copy()

                deptos_i = sorted(df_dep_i["Departamento"].dropna().unique())
                depto_sel_i = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_i,
                    key="pres_ing_depto"
                )

                df_fil_di = df_dep_i[df_dep_i["Departamento"] == depto_sel_i]

                if df_fil_di.empty:
                    st.warning("Sin datos para este departamento.")
                else:
                    metrica_total(df_fil_di, "valor_mm", f"Total Presupuesto · {depto_sel_i}")

                    fig_i_dep = px.treemap(
                        df_fil_di,
                        path=PATH_ING,
                        values="valor_mm",
                        title=f"Composición del presupuesto de ingresos — {depto_sel_i}",
                        color="clas_ofpuj",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_i_dep),
                        use_container_width=True,
                        key="treemap_pres_ing_dep"
                    )

            # ------------------------------------------------------------------
            # INGRESOS – MUNICIPAL
            # ------------------------------------------------------------------
            with t_mun_i:
                df_mun_i = df_ing_clean[
                    df_ing_clean["Tipo de Entidad"] == "Municipio"
                ].copy()

                deptos_mi = sorted(df_mun_i["Departamento"].dropna().unique())
                depto_sel_mi = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_mi,
                    key="pres_ing_mun_depto"
                )

                muns_i = sorted(
                    df_mun_i[df_mun_i["Departamento"] == depto_sel_mi]["Entidad"]
                    .dropna().unique()
                )
                mun_sel_i = st.selectbox(
                    "Selecciona un Municipio",
                    muns_i,
                    key="pres_ing_mun_ent"
                )

                df_fil_mi = df_mun_i[df_mun_i["Entidad"] == mun_sel_i]

                if df_fil_mi.empty:
                    st.warning("Sin datos para este municipio.")
                else:
                    metrica_total(df_fil_mi, "valor_mm", f"Total Presupuesto · {mun_sel_i}")

                    fig_i_mun = px.treemap(
                        df_fil_mi,
                        path=PATH_ING,
                        values="valor_mm",
                        title=f"Composición del presupuesto de ingresos — {mun_sel_i}",
                        color="clas_ofpuj",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_i_mun),
                        use_container_width=True,
                        key="treemap_pres_ing_mun"
                    )

        # =========================================================================
        # GASTOS 2025
        # =========================================================================
        with tab_gast_p:
            st.subheader("Programación de Gastos 2025")

            # Definir columnas de profundidad disponibles en gastos
            # col_1 existe solo en gastos; se usa como raíz de la jerarquía
            COLS_GASTO_RAW = ["col_1", "col_2", "col_3", "col_4", "col_5", "col_6"]
            COL_VAL_G = "Apropiación Definitiva"

            # Detectar cuáles columnas de path realmente existen en el archivo
            PATH_GAST = [c for c in COLS_GASTO_RAW if c in df_gast.columns]

            df_gast_clean = limpiar_path(df_gast, PATH_GAST)
            df_gast_clean["valor_mm"] = df_gast_clean[COL_VAL_G] / 1_000_000_000

            # Sub-tabs territoriales
            t_dep_g, t_mun_g = st.tabs(["Departamental", "Municipal"])

            # ------------------------------------------------------------------
            # GASTOS – DEPARTAMENTAL
            # ------------------------------------------------------------------
            with t_dep_g:
                df_dep_g = df_gast_clean[
                    df_gast_clean["Tipo de Entidad"] == "Departamento"
                ].copy()

                deptos_g = sorted(df_dep_g["Departamento"].dropna().unique())
                depto_sel_g = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_g,
                    key="pres_gast_depto"
                )

                df_fil_dg = df_dep_g[df_dep_g["Departamento"] == depto_sel_g]

                if df_fil_dg.empty:
                    st.warning("Sin datos para este departamento.")
                else:
                    metrica_total(df_fil_dg, "valor_mm", f"Total Apropiación · {depto_sel_g}")

                    fig_g_dep = px.treemap(
                        df_fil_dg,
                        path=PATH_GAST,
                        values="valor_mm",
                        title=f"Composición del presupuesto de gastos — {depto_sel_g}",
                        color="col_1",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_g_dep),
                        use_container_width=True,
                        key="treemap_pres_gast_dep"
                    )

            # ------------------------------------------------------------------
            # GASTOS – MUNICIPAL
            # ------------------------------------------------------------------
            with t_mun_g:
                df_mun_g = df_gast_clean[
                    df_gast_clean["Tipo de Entidad"] == "Municipio"
                ].copy()

                deptos_mg = sorted(df_mun_g["Departamento"].dropna().unique())
                depto_sel_mg = st.selectbox(
                    "Selecciona un Departamento",
                    deptos_mg,
                    key="pres_gast_mun_depto"
                )

                muns_g = sorted(
                    df_mun_g[df_mun_g["Departamento"] == depto_sel_mg]["Entidad"]
                    .dropna().unique()
                )
                mun_sel_g = st.selectbox(
                    "Selecciona un Municipio",
                    muns_g,
                    key="pres_gast_mun_ent"
                )

                df_fil_mg = df_mun_g[df_mun_g["Entidad"] == mun_sel_g]

                if df_fil_mg.empty:
                    st.warning("Sin datos para este municipio.")
                else:
                    metrica_total(df_fil_mg, "valor_mm", f"Total Apropiación · {mun_sel_g}")

                    fig_g_mun = px.treemap(
                        df_fil_mg,
                        path=PATH_GAST,
                        values="valor_mm",
                        title=f"Composición del presupuesto de gastos — {mun_sel_g}",
                        color="col_1",
                    )
                    st.plotly_chart(
                        estilo_treemap(fig_g_mun),
                        use_container_width=True,
                        key="treemap_pres_gast_mun"
                    )
###########################################################################################################################
#Descargas
elif menu == "Descarga de datos":
    st.header("Descarga de datos")

    base_dir = Path(__file__).parent.parent

    def convertir_xlsx(ruta_parquet):
        df = pd.read_parquet(ruta_parquet)
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)
        return buffer.getvalue()

    datasets = [
        {
            "titulo":  "Ingresos territoriales",
            "archivo": base_dir / "data" / "ingresos_ipc_pop.parquet",
            "nombre":  "ingresos_ipc_pop.xlsx",
            "boton":   "Descargar datos completos (xlsx)",
        },
        {
            "titulo":  "Gastos territoriales",
            "archivo": base_dir / "data" / "ejecucion_deflactada_mun.parquet",
            "nombre":  "ejecucion_deflactada_mun.xlsx",
            "boton":   "Descargar datos completos (xlsx)",
        },
        {
            "titulo":  "Sistema General de Participaciones (SGP)",
            "archivo": base_dir / "data" / "datos_sgp_pib_ic.parquet",
            "nombre":  "datos_sgp_pib_ic.xlsx",
            "boton":   "Descargar datos completos (xlsx)",
        },
    ]

    for ds in datasets:
        st.subheader(ds["titulo"])
        if ds["archivo"].exists():
            st.download_button(
                label=ds["boton"],
                data=convertir_xlsx(ds["archivo"]),
                file_name=ds["nombre"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=ds["nombre"],
            )
        else:
            st.warning(f"Archivo no disponible: {ds['archivo'].name}")
        st.divider()

        st.write("Base dir:", base_dir)

       