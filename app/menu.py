import streamlit as st
import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")


from pages import ingresos, gastos, treemap, ejecucion, pgn, anteproyecto, descarga,recaudo

def menu():
    opcion = st.radio(
        "",
        [
            "Main",
            "Ingresos",
            "Gastos",
            "Treemap",
            "Ejecución histórica",
            "Recaudo histórico",
            "PGN 2026",
            "Anteproyecto 2027",
            "Descarga de datos"
        ],
        horizontal=True
    )

    if opcion == "Main":
        st.title("PEPE Territorial")
        st.write("Página principal")

    elif opcion == "Ingresos":
        ingresos.show()

    elif opcion == "Gastos":
        gastos.show()

    elif opcion == "Treemap":
        treemap.show()

    elif opcion == "Ejecución histórica":
        ejecucion.show()

    elif opcion == "Recaudo histórico":
        recaudo.show()
       
    elif opcion == "PGN 2026":
        pgn.show()

    elif opcion == "Anteproyecto 2027":
        anteproyecto.show()

    elif opcion == "Descarga de datos":
        descarga.show()