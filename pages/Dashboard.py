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
import plotly.graph_objects as go
from datetime import datetime
from wordcloud import WordCloud


from ipywidgets import interact, IntRangeSlider




def dashboard():
    data = pd.read_csv("data/data_APP.csv")
    st.title('Estadísticas de Intervenciones')
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

    data2 = pd.read_csv("data/General_data.csv")
    data2 = data2[~data2.applymap(lambda x: x == 'Response').any(axis=1)]
    data2 = data2[~data2.applymap(lambda x: x == '3+').any(axis=1)]

    data2.head() 
    columnas_seleccionadas = ['Fecha Intervención', 'Fecha de Nacimiento','Género','Exfumador/a','Fumador/a',
                          'Patología Sistémica','Localización','Tipo de edentulismo','Duración de la intervención quirúrgica']

# Crear un nuevo DataFrame con las columnas seleccionadas
    data2 = data2[columnas_seleccionadas]

    c1, c2, c3 = st.columns(3)

    with c1:
        categories = data2['Género'].dropna()
        durations = data2['Duración de la intervención quirúrgica'].dropna()

# Crear un DataFrame
        data_G = pd.DataFrame({
            'Género': categories,
            'Duración': durations
        })

# Eliminar filas con categorías o valores NaN
        data_G.dropna(inplace=True)

# Preparar datos para el gráfico de barras apiladas
        stacked_data = data_G.groupby(['Género', 'Duración']).size().unstack(fill_value=0)

# Definir colores personalizados para cada rango de duración
        colors = {
    '0-5 minutos': '#020659',
    '5-10 minutos': '#2155BF',
    '10-20 minutos': '#71CEF2',
    '20-40 minutos': '#58A8D9',
    '40-60 minutos': '#4393D9',
    '60-90 minutos': '#020659',
    '90-120 minutos': '#2155BF',
    '120-180 minutos': '#71CEF2',
    '>180 minutos': '#58A8D9'
}

# Crear el gráfico de barras apiladas
        fig = go.Figure()

        for duration in stacked_data.columns:
            fig.add_trace(go.Bar(
            x=stacked_data.index,
            y=stacked_data[duration],
            name=duration,
            marker_color=colors[duration]  # Usar colores personalizados
            ))

# Añadir características del gráfico
        fig.update_layout(
           barmode='stack',
           title='Distribution of Intervention Duration by Gender',
           xaxis_title='Gender',
           yaxis_title='Count of Intervention',
           template='plotly_white')
        
        st.plotly_chart(fig)


        with c2:
            data_w = data2['Tipo de edentulismo'].dropna()


            text = ' '.join(data_w.astype(str))

# Definir el colormap deseado
            colormap = 'Blues'  # Cambia esto a cualquier colormap que prefieras

# Generar el WordCloud
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap=colormap).generate(text)

# Mostrar el WordCloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Type of edentulism')
            st.pyplot(plt)


        with c3:
            data_l = data2['Localización'].dropna()


            unique, counts = np.unique(data_l[~pd.isnull(data_l)], return_counts=True)


            colors = ['#2155BF', '#71CEF2']  # Azul oscuro y Azul claro

# Crear el gráfico de dona
            fig = go.Figure(data2=[go.Pie(
                labels=unique,
                values=counts,
                hole=.4,  # Tamaño del agujero central, haciendo que parezca una dona
                marker_colors=colors,  # Colores de las secciones
                hoverinfo='label+percent',  # Mostrar etiquetas y porcentajes al pasar el mouse
                textinfo='label+value+percent'  # Mostrar información en el gráfico
                )])

# Añadir título
            fig.update_layout(
                title={
                'text': "Location Distribution",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                template='plotly_white',  # Usar un fondo blanco para más claridad
                font=dict(
                family="Arial, sans-serif",
                size=12,
                color="black"
                           )
            )
            st.plotly_chart(fig)


        

# Mostrar el nuevo DataFrame
   


     
    data['Fecha.de.Nacimiento'] = pd.to_datetime(data['Fecha.de.Nacimiento'], dayfirst=True, errors='coerce')

# Calcular la edad en años
    data['Edad'] = (pd.Timestamp.now() - data['Fecha.de.Nacimiento']).dt.days // 365

    data.dropna(subset=['Tipo.de.Intervención.Quirúrgica', 'Edad', 'Duración.de.la.intervención.quirúrgica'], inplace=True)


# Crear el gráfico
    fig = px.bar(
    data, 
    x='Tipo.de.Intervención.Quirúrgica', 
    y='Edad', 
    color='Duración.de.la.intervención.quirúrgica',
    title='Edad por Tipo de Intervención y Duración',
    labels={
        'Edad': 'Edad en Años', 
        'Tipo.de.Intervención.Quirúrgica': 'Tipo de Intervención', 
        'Duración.de.la.intervención.quirúrgica': 'Duración de Intervención'
    }
)
# Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
    

    data = pd.read_excel('data/datos_APP1.xlsx', index_col=0)

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
