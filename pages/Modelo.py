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
    'Tipo de intervencióm quirurgica': {'Cirugía Dentoalveolar': 0, 'Cirugía Peri-implantaria': 1, 'Implantología Bucal':2},

    'Tipo de cirugía': {0: 0, 'Cirugía combinada (regenerativa + implantoplastia)': 1, 'Cirugía resectiva': 4, 'Cirugía regenerativa': 3},

    'Material de regeneración': {'Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)': 1,'0': 0},


    'Tipo de prótesis': {'0':0, 'Prótesis híbrida':2, 'Sobredentadura':4, 'Puente sobre implantes':3},

    'Implante 1 defecto tipo 1 infraóseo': {'0': 0, 'No':3, 'Id':1},

    'Alcohol': {'No consumo': 2, 'Consumo moderado':1, 'Consumo elevado':0},


    'Caracteristicas del implante' : {0:0, 12:1, '16.0': 3},

    'Implante 1 defecto tipo 2 supraóseo.' : {0:0,  "Sí" : 2, "No": 1},

    'Número de implantes' : {0:0, 2:4, 1:1, 6:6, '1.0' : 6},
    
    'Características del implante 2' :  {0:0, 34:1, 42:7}

    }




    modelo = load('data/modelo_entrenado_DEFi.joblib')

    with st.form("Model-Survey"):
        inter = st.selectbox("Tipo de Intervencion Quirúrgica", ("Cirugía Dentoalveolar", "Cirugía Peri-implantaria", "Implantología Bucal"))
        cirugia = st.selectbox("Tipo de Cirugia", (0, "Cirugía combinada (regenerativa + implantoplastia)", "Cirugía de acceso", "Cirugía resectiva", "Cirugía regenerativa"))
        mat_regen = st.selectbox("Material de Regeneracion", ("0", "Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)"))
        num_implante = st.selectbox("Número de implantes",  (0, 1, 2, '1.0'))
        tipo_prot = st.selectbox("Tipo de Protesis", (0, "Corona unitaria", "Puente sobre implantes", "Prótesis híbrida", "Sobredentadura", "Full-arch metal-cerámica"))
        caract_imp = st.selectbox("Características del implante", (0, 12, '16.0'))
        def_suposeo = st.selectbox("Defecto Supraoseo Implante 1", (0, "Sí", "No"))
        caract_imp2 = st.selectbox("Caracteristicas del implante 2", (0, 34, 42))
        de_oseo = st.selectbox("Defecto Infraóseo", (0, "No", "Ib"))
        alcohol = st.selectbox("Alcohol", ("No consumo", "Consumo moderado", "Consumo elevado"))


        submitted = st.form_submit_button(label="Submit", use_container_width=False)
    
    if submitted:
        # Store the selected options in a dictionary or any other data structure
        survey_results = {
            "Tipo de cirugia": cirugia,
            "Tipo de prótesis": tipo_prot,
            "Número de implantes": num_implante,
            "Tipo de intervencióm quirurgica" : inter,
            "Alcohol": alcohol,
            "Material de regeneración": mat_regen,
            "Caracteristicas del implante": caract_imp,
            "Características del implante 2": caract_imp2,
            "Implante 1 defecto tipo 1 infraóseo": de_oseo,
            "Implante 1 defecto tipo 2 supraóseo." : def_suposeo,
        }

        

        st.session_state.submissions.append(survey_results)
        #results = pd.DataFrame(survey_results)
        results = pd.DataFrame([survey_results])
        st.write(results)
        
        data = results.replace(mappings, inplace = True )
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