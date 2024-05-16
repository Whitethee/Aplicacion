from numpy import NaN
import streamlit as st
import pandas as pd
import pickle
from datacleaner import autoclean
from joblib import load


def clasificador():

    if 'submissions' not in st.session_state:
        st.session_state.submissions = []

    model = load('data/modelo_random_forest.joblib')

    


    with st.form("Clasificador-Survey"):
        genero = st.selectbox("Género", ("Hombre", "Mujer"))
        edad = st.number_input("Edad")
        alc = st.selectbox("Alcohol", ("No consumo", "Consumo moderado", "Consumo elevado"))
        hipart = st.checkbox("Hipertensión Arterial")
        hipcol = st.checkbox("Hipercolesterolemia")
        fumador = st.checkbox("Fumador/a")
        diab2 = st.checkbox("Diabetes II")
        diab1 = st.checkbox("Diabetes I")
        osteo = st.checkbox("Osteoporosis")
        quimio = st.checkbox("Quimioterapia")
        intquir = st.selectbox("Tipo de Intervención Quirúrgica", ("Cirugía Dentoalveolar", "Cirugía Peri-implantaria", "Implantología Bucal"))
        tipocir = st.selectbox("Tipo de cirugía", ("Cirugía combinada (regenerativa + implantoplastia)", "Cirugía de acceso", "Cirugiá resectiva", "Cirugía regenerativa"))
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
            "Edad": int(edad),
        }

        st.session_state.submissions.append(sur_res)
        res = pd.DataFrame([sur_res])
        data = autoclean(res)
        st.write(data)
        #response = model.predict(data)
        st.write(sur_res)
        st.session_state.user_input = ""
        #st.write(f"la operación tendra una dificultad de {response}")



clasificador()

