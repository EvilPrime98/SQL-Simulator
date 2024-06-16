import streamlit as st
import sqlite3
import pandas as pd
import os
import subprocess

def ejecutar_consulta(query, nombre_bd):
    if not os.path.exists(nombre_bd):
        conn = sqlite3.connect(nombre_bd)
        conn.close()
    
    conn = sqlite3.connect(nombre_bd)
    c = conn.cursor()
    try:
        for statement in query.split(';'):
            if statement.strip():
                c.execute(statement)
        if query.strip().lower().startswith('select'):
            datos = c.fetchall()
            columnas = [desc[0] for desc in c.description]
            df = pd.DataFrame(datos, columns=columnas)
            conn.close()
            return df
        elif query.strip().lower().startswith('create table'):
            conn.commit()
            conn.close()
            return None
        else:
            conn.commit()
            conn.close()
            return "Operación realizada exitosamente."
    except sqlite3.Error as e:
        conn.close()
        return f"Error: {e}"

st.title('Simulador de SQL')

nombre_bd = st.text_input("Ingrese el nombre de la base de datos:", "basededatos.db")
consulta_sql = st.text_area("Escribe tu consulta SQL aquí:", height=200)

if st.button('Ejecutar'):
    if consulta_sql.strip():
        resultado = ejecutar_consulta(consulta_sql, nombre_bd)
        if isinstance(resultado, pd.DataFrame):
            st.dataframe(resultado)
        elif resultado is None:
            st.success("Operación realizada exitosamente.")
        else:
            st.error(resultado)
    else:
        st.error("Por favor, escribe una consulta SQL.")