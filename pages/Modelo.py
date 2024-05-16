import streamlit as st
from joblib import load
import pandas as pd
from datacleaner import autoclean
import pickle

def surveyMod():

    if 'submissions' not in st.session_state:
        st.session_state.submissions = []


    mappings = {
    'Tipo Intervencion': {'Cirugía Dentoalveolar': 0, 'Cirugía Peri-implantaria': 1, 'Implantología Bucal':2},

    'Tipo de Cirugia': {'Cirugía combinada (regenerativa + implantoplastia)': 0, 'Cirugía resectiva': 1, 'Cirugía de acceso': 2, 'Cirugía regenerativa': 3},

    'Material de regeneracion': {'Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)': 1,'0': 0},

    'Numero de implante': {'1.0': 1},

    'Tipo de Pprotesis sobre implante': {'Corona unitaria': 1, '0':0, 'Prótesis híbrida':2, 'Sobredentadura':3, 'Puente sobre implantes':4},

    'Caracteristicas del implante': {'16.0': 16},

    'Implante 1 defecto tipo 1 infraóseo': {'0': 0, 'No':1, 'Ic':2, 'Id':3},

    'Alcohol': {'No consumo': 0, 'Consumo moderado':1, 'Consumo elevado':2},

    'Medicacion actual': {'No': 0, 'Sí':1}
    }




    modelo = load('data/modelo_entrenado_Tiempo.joblib')

    with st.form("Model-Survey"):
        inter = st.selectbox("Tipo de Intervencion", ("Cirugía Dentoalveolar", "Cirugía Peri-implantaria", "Implantología Bucal"))
        cirugia = st.selectbox("Tipo de Cirugia", ("Cirugía combinada (regenerativa + implantoplastia)", "Cirugía de acceso", "Cirugía resectiva", "Cirugía regenerativa"))
        mat_regen = st.selectbox("Material de Regeneracion", ("0", "Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)"))
        num_implante = st.selectbox("Número de implantes",  (1, 2, 3, 4, 5, 6))
        tipo_prot = st.selectbox("Tipo de Protesis", (0, "Corona unitaria", "Puente sobre implantes", "Prótesis híbrida", "Sobredentadura", "Full-arch metal-cerámica"))
        caract_imp = st.selectbox("Características del implante", ('0', '12', '21', '36', '23', '45', '16.0'))
        de_oseo = st.selectbox("Defecto Infraóseo", ("Id", "No", "Implante 1 - Defecto tipo I (infraóseo)", "Ib", "Ic", "Ie"))
        alcohol = st.selectbox("Alcohol", ("No consumo", "Consumo moderado", "Consumo elevado"))
        medactual = st.selectbox("Medicación Actual", ("No", "Sí"))
        pos_imp = st.selectbox("Posición del Implante", ('0', '35', '14', '16', '36', '25', '37', '27'))

        submitted = st.form_submit_button(label="Submit", use_container_width=False)
    
    if submitted:
        # Store the selected options in a dictionary or any other data structure
        survey_results = {
            "Tipo Intervencion" : inter,
            "Tipo de Cirugia": cirugia,
            "Material de regeneracion": mat_regen,
            "Numero de implante": num_implante,
            "Tipo de Pprotesis sobre implante": tipo_prot,
            "Caracteristicas del implante": caract_imp,
            "Implante 1 defecto tipo 1 infraóseo": de_oseo,
            "Alcohol": alcohol,
            "Medicacion actual": medactual,
            "Posicion del implante": pos_imp
        }

        st.session_state.submissions.append(survey_results)
        #results = pd.DataFrame(survey_results)
        results = pd.DataFrame([survey_results])
        data = results.replace(mappings, inplace=True)
        res = modelo.predict(data)
        res = res
       


        c1, c2 = st.columns(2)

        with c1:
            st.write((f"El resultado es {res}"))

        with c2:
            st.image("verdecirc.jpg", use_column_width="auto", output_format="PNG")


        
surveyMod()