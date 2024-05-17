import streamlit as st
from joblib import load
import pandas as pd
from datacleaner import autoclean
import pickle

def surveyMod():


    st.title("Predicción de Tiempo Quirúrgico")

    st.write("________________________________________________________________")

    descp = f"""
    Nuestro modelo **PredictOR** utiliza técnicas avanzadas de **ciencia de datos** para 
    predecir la duración de las intevenciones quirúrgicas. <br>
    Con esta herramienta, podemos mejorar la planificación y programación
    de las operaciones, asegurando un uso más eficiente de nuestras camillas y recursos
    """
    st.markdown(descp, unsafe_allow_html=True)

    if 'submissions' not in st.session_state:
        st.session_state.submissions = []


    mappings = {
    'Tipo.de.Intervención.Quirúrgica': {'Cirugía Dentoalveolar': 0, 'Cirugía Peri-implantaria': 1, 'Implantología Bucal':2},

    'Tipo.de.cirugía': {0: 0, 'Cirugía combinada (regenerativa + implantoplastia)': 1, 'Cirugía resectiva': 4, 'Cirugía de acceso': 2, 'Cirugía regenerativa': 3},

    'X.Qué.material.de.regeneración.ha.sido.utilizado.': {'Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)': 1,'0': 0},


    'Tipo.de.prótesis.sobre.implantes': {'Corona unitaria': 1, '0':0, 'Prótesis híbrida':2, 'Sobredentadura':4, 'Puente sobre implantes':3},

    'Implante.1...Defecto.tipo.I..infraóseo..2': {'0': 0, 'No':3, 'Ic':1, 'Id':2},

    'Alcohol': {'No consumo': 0, 'Consumo moderado':1, 'Consumo elevado':2},


    'Caracteristicas.del.implante' : {0:0, 12:1, 21:3, 36:5, 23:4, 45:6, 16.0:2 },

    'Implante.1...Defecto.tipo.II..supraóseo.' : {0:0,  "Sí" : 2, "No": 1},

    'Número.de.implantes' : {0:0, 3:4, 2:3, 1:1, 6:6, 4:5},
    
    'Características.del.implante.2' :  {0: 0, 12: 1, 32:5, 34:6, 36:7, 22:3, 21:2, 26:4, 42:8}

    }




    modelo = load('data/modelo_entrenado_DEF.joblib')

    with st.form("Model-Survey"):
        inter = st.selectbox("Tipo de Intervencion Quirúrgica", ("Cirugía Dentoalveolar", "Cirugía Peri-implantaria", "Implantología Bucal"))
        cirugia = st.selectbox("Tipo de Cirugia", (0, "Cirugía combinada (regenerativa + implantoplastia)", "Cirugía de acceso", "Cirugía resectiva", "Cirugía regenerativa"))
        mat_regen = st.selectbox("Material de Regeneracion", ("0", "Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)"))
        num_implante = st.selectbox("Número de implantes",  (1, 2, 3, 4, 5, 6))
        tipo_prot = st.selectbox("Tipo de Protesis", (0, "Corona unitaria", "Puente sobre implantes", "Prótesis híbrida", "Sobredentadura", "Full-arch metal-cerámica"))
        caract_imp = st.selectbox("Características del implante", (0, 12, 21, 36, 23, 4, 16.0))
        def_suposeo = st.selectbox("Defecto Supraoseo Implante 1", (0, "Sí", "No"))
        caract_imp2 = st.selectbox("Caracteristicas del implante 2", (0, 12, 21, 22, 26, 32, 34, 36, 42))
        de_oseo = st.selectbox("Defecto Infraóseo", (0, "No", "Ib", "Ic"))
        alcohol = st.selectbox("Alcohol", ("No consumo", "Consumo moderado", "Consumo elevado"))


        submitted = st.form_submit_button(label="Submit", use_container_width=False)
    
    if submitted:
        # Store the selected options in a dictionary or any other data structure
        survey_results = {
            "Tipo.de.cirugía": cirugia,
            "Tipo.de.prótesis.sobre.implantes": tipo_prot,
            "Número.de.implantes": num_implante,
            "Tipo.de.Intervención.Quirúrgica" : inter,
            "Alcohol": alcohol,
            "X.Qué.material.de.regeneración.ha.sido.utilizado.": mat_regen,
            "Caracteristicas.del.implante": caract_imp,
            "Características.del.implante.2": caract_imp2,
            "Implante.1...Defecto.tipo.I..infraóseo..2": de_oseo,
            "Implante.1...Defecto.tipo.II..supraóseo." : def_suposeo,
        }

        

        st.session_state.submissions.append(survey_results)
        #results = pd.DataFrame(survey_results)
        results = pd.DataFrame([survey_results])
        st.write(results)
        for i in results.columns:
            data = i.replace(mappings, inplace= True)
            st.write(data)
        data = results.replace(mappings, inplace=True)
        st.write(data)
        res = modelo.predict(data)
        res = res
       


        c1, c2 = st.columns(2)

        with c1:
            st.write((f"El resultado es {res}"))

        with c2:
            st.image("verdecirc.jpg", use_column_width="auto", output_format="PNG")


        
surveyMod()