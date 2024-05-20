
import markdown
import streamlit as st


st.set_page_config(
    page_title="Software de Predicción Quirúrgica",
    page_icon="🏠",
    layout = "wide"
)
st.title("Plataforma de Gestión Clínica")
st.write("________________________________________________")
st.write("Bienvenido a nuestra plataforma de gestión y agendado de pacientes. Nuestro objetivo es optimizar el uso de nuestras camillas y permitir que más estudiantes puedan recibir la formación práctica que necesitan.")
st.write("Navega por nuestra aplicación para conocer más sobre cómo clasificamos y gestionamos las intervenciones dentales, y cómo utilizamos datos para mejorar la eficiencia en nuestra clínica.")

st.write("__________________________________________________________________________________")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Descripción")
    st.markdown("""
                Somos un equipo de estudiantes apasionados de la Universitat Politècnica de València, especializados en tecnología y análisis de datos.
                 Nuestro grupo está comprometido con la innovación y la aplicación práctica de nuestros conocimientos en ciencias de la computación para
                resolver problemas reales y mejorar la eficiencia en diferentes ámbitos,
                especialmente en el sector de la salud
                """)


with c2:
    st.subheader("¿Quienes somos?")
    st.markdown("""
                Desarrollada por un equipo de estudiantes dedicados de la Universitat Politècnica de València,
                nuestra aplicación web surge como una solución innovadora dirigida a optimizar y transformar la gestión de clínicas dentales.
                Nuestro proyecto se articula en dos componentes principales que trabajan de manera sinérgica para ofrecer resultados excepcionales:

**Dashboard de Gestión Quirúrgica**: Esta herramienta integral proporciona una visión completa y actualizada de las intervenciones quirúrgicas.
               A través de interfaces intuitivas, ofrecemos acceso a datos críticos como perfiles de pacientes, detalles de medicación e historiales de procedimientos, todo en tiempo real. 
               Este enfoque no solo mejora la eficiencia operativa, sino que también eleva el nivel de cuidado al paciente, permitiendo a los profesionales tomar decisiones informadas rápidamente.
                
**Predicción de Duración de Operaciones**: Gracias a nuestro avanzado sistema de predicción basado en un cuestionario de diez preguntas, nuestra aplicación estima la duración de las cirugías futuras.
                Esta funcionalidad es clave para mejorar la planificación y gestión del tiempo dentro de las clínicas, permitiendo una asignación más eficiente de recursos y reduciendo las esperas innecesarias para los pacientes.
Nuestra aplicación está diseñada no solo para responder a las necesidades actuales de las clínicas dentales sino también para adaptarse a los cambios y desafíos futuros del sector de la salud dental.
                Nos esforzamos por ser pioneros en el campo, proporcionando herramientas que hacen una diferencia tangible en la vida diaria de los profesionales y sus pacientes
                """)
    
st.write("______________________________________________________________")

col1, col2, col3, col4, col5= st.columns(5)

with col1:
    st.image('data/manue-modified.png', use_column_width="auto", output_format="PNG")

with col2:
    st.image('data/jezabel-modified.png', use_column_width="auto", output_format="PNG")

with col3:
    st.image('data/jazmina-modified.png', use_column_width="auto", output_format="PNG")

with col4:
    st.image('data/euge-modified.png', use_column_width="auto", output_format="PNG")

with col5:
    st.image('data/carla-modified.png', use_column_width="auto", output_format="PNG")
