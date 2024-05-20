
from numpy import NaN
import streamlit as st
import pandas as pd
import pickle
from datacleaner import autoclean
from joblib import load

st.set_page_config(page_title= "Clasificador de Intervenciones",
                   page_icon=	"🎏")

def clasificador():


    st.title("Clasificación de Intervenciones")
    st.write("__________________________________________________")

    desc = f"""
    Utliza nuestro cuestionario de **10** preguntas para clasificar la complejidad de las intervenciones 
    dentales. Este sistema nos ayuda a organizar mejor las operaciones, categorizandolas en
    **muy fácil**, **fácil**, **moderada**, **difíciles** o **muy difíciles**. <br>
    Así, podemos asignar los casos más adecuado a nuestros estudiantes y
    asegurar una experiencia de aprendizaje óptima
    """
    st.markdown(desc, unsafe_allow_html=True)

    if 'submissions' not in st.session_state:
        st.session_state.submissions = []

    model = load('data/modelo_random_forest.joblib')

    mappings = {
    'Género': {'Mujer': 0, 'Hombre': 1},
    'Alcohol': {'No consumo': 0, 'Consumo moderado': 1, 'Consumo elevado': 2},
    'Hipertensión Arterial': {'no': 0, 'Hipertensión Arterial': 1},
    'Hipercolesterolemia': {'no': 0, 'Hipercolesterolemia': 1},
    'Fumador/a': {'no': 0, 'Fumador/a': 1},
    'Diabetes II': {'no': 0, 'Diabetes II': 1},
    'Diabetes I': {'no': 0, 'Diabetes I': 1},
    'Osteoporosis': {'no': 0, 'Osteoporosis': 1},
    'Quimioterapia': {'no': 0, 'Quimioterapia': 1},
    'Tipo de Intervención Quirúrgica': {'Cirugía Dentoalveolar': 0, 
                                        'Cirugía Peri-implantaria': 1,
                                       'Implantología Bucal':2},
    'Tipo de cirugía': {'no': 0, 
                        'Cirugía resectiva': 1, 
                        'Cirugía combinada (regenerativa + implantoplastia)': 2,
                       'Cirugía de acceso':3,
                       'Cirugía regenerativa':4},
    'Duración de la intervención quirúrgica': {'0-5 minutos': 0,
                                               '5-10 minutos': 1, 
                                               '10-20 minutos': 2,
                                               '20-40 minutos': 3, 
                                               '40-60 minutos': 4,
                                               '60-90 minutos': 5,
                                               '90-120 minutos': 6,
                                               '120-180 minutos': 7,
                                              '>180 minutos': 8 },
    'Clasificación Dificultad': {'Muy Fácil': 0, 'Fácil': 1, 'Moderada': 2, 'Difícil': 3}
    }


    


    with st.form("Clasificador-Survey"):
        genero = st.selectbox("Género", ("Hombre", "Mujer"))
        #edad = st.number_input("Edad")
        alc = st.selectbox("Alcohol", ("No consumo", "Consumo moderado", "Consumo elevado"))
        cl1, cl2, cl3 = st.columns(3)
        with cl1:
           hipart = st.checkbox("Hipertensión Arterial")
           hipcol = st.checkbox("Hipercolesterolemia")
           fumador = st.checkbox("Fumador/a")
        with cl2:
           diab2 = st.checkbox("Diabetes II")
           diab1 = st.checkbox("Diabetes I")
        with cl3:
           osteo = st.checkbox("Osteoporosis")
           quimio = st.checkbox("Quimioterapia")
        intquir = st.selectbox("Tipo de Intervención Quirúrgica", ("Cirugía Dentoalveolar", "Cirugía Peri-implantaria", "Implantología Bucal"))
        tipocir = st.selectbox("Tipo de cirugía", ("Cirugía combinada (regenerativa + implantoplastia)", "Cirugía de acceso", "Cirugía resectiva", "Cirugía regenerativa"))
        duracion = st.selectbox("Duración de la intervención quirúrgica", ("0-5 minutos", "10-20 minutos", "20-40 minutos", "40-60 minutos", "60-90 minutos", "90-120 minutos", "120-180 minutos"))

        sub = st.form_submit_button("Predecir", use_container_width=False)

        if hipart:
            hipart = "Hipertensión Arterial"
        else: hipart = 0

        if hipcol:
            hipcol = "Hipercolesterolemia"
        else: hipcol = 0

        if fumador:
            fumador = "Fumador/a"
        else: fumador = 0

        if diab2:
            diab2 = "Diabetes II"
        else: diab2 = 0

        if diab1:
            diab1 = "Diabetes I"
        else: diab1 = 0

        if osteo:
            osteo = "Osteoporosis"
        else: osteo = 0

        if quimio:
            quimio = "Quimioterapia"
        else: quimio = 0
    

    if sub:
        sur_res = {
            "Género": genero,
            "Alcohol": alc,
            "Hipertensión Arterial": hipart,
            "Hipercolesterolemia": hipcol,
            "Fumador/a": fumador,
            "Diabetes II": diab2,
            "Diabetes I": diab1,
            "Osteoporosis": osteo,
            "Quimioterapia": quimio,
            "Tipo de Intervención Quirúrgica": intquir,
            "Tipo de cirugía": tipocir,
            "Duración de la intervención quirúrgica": duracion,
            
        }

        st.session_state.submissions.append(sur_res)
        

        # Convertimos los datos de la encuesta en DataFrame

        res = pd.DataFrame([sur_res])
        res.replace(mappings, inplace=True)

        res.replace('na', pd.NA, inplace=True)
        res.replace('no', pd.NA, inplace=True)
        res.dropna(inplace=True) 
        st.write("En el siguiente DataFrame se exponen los datos usados para predecir")
        st.write(res)
        
        response = model.predict(res)
        resp = response[0]
        #st.write(sur_res)
        st.write("_____________________________________________________________")
        c1, c2 = st.columns(2)


        with c1:
            st.markdown(f"""
                    La operación tendra una dificultad  **{resp}**
                    """)
        
        with c2:
            if resp == "Muy Fácil":
                st.image('data/very_easy.jpeg', use_column_width="auto", output_format="JPEG")
            if resp == "Fácil":
                st.image('data/easy.jpeg', use_column_width="auto", output_format="JPEG")
            if resp == "Moderada":
                st.image('data/moderade.jpeg', use_column_width="auto", output_format="JPEG")
            if resp == "Difícil":
                st.image('data/difficult.jpeg', use_column_width="auto", output_format="JPEG")
            if resp == "Muy Difícil":
                st.image('data/very_diff.jpeg', use_column_width="auto", output_format="JPEG")


    


clasificador()

