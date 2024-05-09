import streamlit as st
import pandas as pd
import json 
import requests
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px
import numpy as np
from datetime import datetime


from ipywidgets import interact, IntRangeSlider




def dashboard():
    data = pd.read_csv("whitethee/aplicacion/main/data/data_APP.csv")
    st.title('Monitor Médico')
    st.markdown("""
# Bienvenido/a al dashboard de nuestra aplicación web

Esta herramienta está diseñada para optimizar el manejo de cirugías bucodentales y se organiza en tres secciones clave:

1. **Intervenciones Quirúrgicas**: Detalles completos sobre los procedimientos realizados, equipos involucrados y resultados.
2. **Pacientes**: Información detallada de cada paciente, incluyendo historial médico y diagnósticos.
3. **Medicación**: Gestión de las medicaciones prescritas, dosificaciones y horarios de administración.

Este dashboard proporciona acceso inmediato a información crítica, facilitando decisiones informadas y mejorando la calidad del cuidado al paciente.
""")
    st.write("____________________________________________________")
   

    st.dataframe(data)



     
    data['Fecha.de.Nacimiento'] = pd.to_datetime(data['Fecha.de.Nacimiento'], errors='coerce')

# Calcular la edad en años
    data['Edad'] = (pd.Timestamp.now() - data['Fecha.de.Nacimiento']).dt.days // 365

# Crear el gráfico
    fig = px.bar(data, x='Tipo.de.Intervención.Quirúrgica', y='Edad', color='Duración.de.la.intervención.quirúrgica',
             title='Edad por Tipo de Intervención y Duración',
             labels={'Edad': 'Edad en Años', 'Tipo.de.Intervención.Quirúrgica': 'Tipo de Intervención', 'Duración.de.la.intervención.quirúrgica': 'Duración de Intervención'})

# Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    

    data = pd.read_excel('whitethee/aplicacion/main/data/datos_APP1.xlsx', index_col=0)

# Convertir la columna de duración a tipo categórico con orden específico
    data['Duración.de.la.intervención.quirúrgica'] = pd.Categorical(
       data['Duración.de.la.intervención.quirúrgica'],
       categories=[
        '0-5 minutos', '5-10 minutos', '10-20 minutos', '20-40 minutos', '40-60 minutos',
        '60-90 minutos', '90-120 minutos', '120-180 minutos', '>180 minutos'
    ],
    ordered=True
)

# Convertir la columna de fecha a datetime
    data['Fecha.Intervención'] = pd.to_datetime(data['Fecha.Intervención'])

# Configuración de Streamlit
    st.title('Distribución de Duraciones de Intervenciones Quirúrgicas')



# Obtener el rango de años del DataFrame
    min_year = int(data['Fecha.Intervención'].dt.year.min())
    max_year = int(data['Fecha.Intervención'].dt.year.max())

# Crear selectores para el año de inicio y el año de finalización en Streamlit
    st.title('Intervenciones Quirúrgicas')
    st.subheader('Selecciona el rango de años')

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.selectbox('Año de inicio', range(min_year, max_year+1), index=0)
    with col2:
        end_year = st.selectbox('Año de finalización', range(min_year, max_year+1), index=(max_year - min_year))




    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    mask = (data['Fecha.Intervención'] >= start_date) & (data['Fecha.Intervención'] <= end_date)
    filtered_data = data.loc[mask]

    data_count = filtered_data['Duración.de.la.intervención.quirúrgica'].value_counts().sort_index()

    plot_data = pd.DataFrame({
    'Duración.de.la.intervención.quirúrgica': data_count.index,
    'Frecuencia': data_count.values
    })

    custom_colors = ['#020659', '#4393D9', '#5BA9D9', '#72CEF2', '#1F50B6', '#334CE2']

    fig = px.bar(
    plot_data,
    x='Duración.de.la.intervención.quirúrgica',
    y='Frecuencia',
    title='Distribución de Duraciones de Intervenciones Quirúrgicas',
    labels={'Duración.de.la.intervención.quirúrgica': 'Duración de la Intervención', 'Frecuencia': 'Frecuencia'},
    color='Duración.de.la.intervención.quirúrgica',
    color_discrete_sequence=custom_colors
)

    fig.update_layout(xaxis_title='Duración de la Intervención', yaxis_title='Frecuencia')

# Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

dashboard()
# %%
