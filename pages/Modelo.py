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


    mapeos = {
    'Tipo de cirugia': {
        0: '0',
        1: 'Cirugía combinada (regenerativa + implantoplastia)',
        4: 'Cirugía resectiva',
        2: 'Cirugía regenerativa'
    },
    'Tipo de prótesis': {
        0: '0',
        2: 'Prótesis híbrida',
        1: 'Puente sobre implantes',
        4: 'Sobredentadura'
    },
    'Número de implantes': {
        0: '0',
        4: '2',
        1: '1',
        6: '1.0'
    },
    'Tipo de intervencióm quirurgica': {
        0: 'Cirugía Dentoalveolar',
        2: 'Implantología Bucal',
        1: 'Cirugía Peri-implantaria'
    },
    'Alcohol': {
        2: 'No consumo',
        1: 'Consumo moderado',
        0: 'Consumo elevado'
    },
    'Material de regeneración': {
        0: '0',
        1: 'Xenoinjerto (Bio-Oss) + Membrana de colágeno reabsorbible (Bio-Gide)'
    },
    'Características del implante': {
        0: '0',
        1: '12',
        3: '16.0'
    },
    'Características del implante 2': {
        0: '0',
        1: '34',
        7: '42'
    },
    'Implante 1 defecto tipo 1 infraóseo': {
        0: '0',
        3: 'No',
        1: 'Id'
    },
    'Implante 1 defecto tipo 2 supraóseo': {
        0: '0',
        2: 'Sí',
        1: 'No'
    }
    # Añade más mapeos si es necesario
}


    modelo = load('data/modelo_entrenado_DEF.joblib')

    with st.form("my_form"):
        st.write("Por favor, responde las siguientes preguntas para predecir la duración de la intervención quirúrgica:")
    
    # Campos para cada característica
        tipo_cirugia = st.selectbox('Tipo de cirugía', options=list(mapeos['Tipo de cirugia'].values()))
        tipo_protesis = st.selectbox('Tipo de prótesis', options=list(mapeos['Tipo de prótesis'].values()))
        num_implantes = st.selectbox('Número de implantes', options=list(mapeos['Número de implantes'].values()))
        tipo_intervencion = st.selectbox('Tipo de intervencióm quirúrgica', options=list(mapeos['Tipo de intervencióm quirurgica'].values()))
        consumo_alcohol = st.selectbox('Alcohol', options=list(mapeos['Alcohol'].values()))
        material_regeneracion = st.selectbox('Material de regeneración', options=list(mapeos['Material de regeneración'].values()))
        caracteristicas_implante = st.selectbox('Características del implante', options=list(mapeos['Características del implante'].values()))
        caracteristicas_implante2 = st.selectbox('Características del implante 2', options=list(mapeos['Características del implante 2'].values()))
        defecto_infraoseo = st.selectbox('Implante 1 defecto tipo 1 infraóseo', options=list(mapeos['Implante 1 defecto tipo 1 infraóseo'].values()))
        defecto_supraoseo = st.selectbox('Implante 1 defecto tipo 2 supraóseo', options=list(mapeos['Implante 1 defecto tipo 2 supraóseo'].values()))
    
    # Botón de envío del formulario
        submitted = st.form_submit_button("Predecir")
    
        if submitted:
        # Transformar las entradas en el formato correcto
            input_data = {
                'Tipo de cirugia': [list(mapeos['Tipo de cirugia'].keys())[list(mapeos['Tipo de cirugia'].values()).index(tipo_cirugia)]],
                'Tipo de prótesis': [list(mapeos['Tipo de prótesis'].keys())[list(mapeos['Tipo de prótesis'].values()).index(tipo_protesis)]],
                'Número de implantes': [list(mapeos['Número de implantes'].keys())[list(mapeos['Número de implantes'].values()).index(num_implantes)]],
                'Tipo de intervencióm quirurgica': [list(mapeos['Tipo de intervencióm quirurgica'].keys())[list(mapeos['Tipo de intervencióm quirurgica'].values()).index(tipo_intervencion)]],
                'Alcohol': [list(mapeos['Alcohol'].keys())[list(mapeos['Alcohol'].values()).index(consumo_alcohol)]],
                'Material de regeneración': [list(mapeos['Material de regeneración'].keys())[list(mapeos['Material de regeneración'].values()).index(material_regeneracion)]],
                'Características del implante': [list(mapeos['Características del implante'].keys())[list(mapeos['Características del implante'].values()).index(caracteristicas_implante)]],
                'Características del implante 2': [list(mapeos['Características del implante 2'].keys())[list(mapeos['Características del implante 2'].values()).index(caracteristicas_implante2)]],
                'Implante 1 defecto tipo 1 infraóseo': [list(mapeos['Implante 1 defecto tipo 1 infraóseo'].keys())[list(mapeos['Implante 1 defecto tipo 1 infraóseo'].values()).index(defecto_infraoseo)]],
                'Implante 1 defecto tipo 2 supraóseo': [list(mapeos['Implante 1 defecto tipo 2 supraóseo'].keys())[list(mapeos['Implante 1 defecto tipo 2 supraóseo'].values()).index(defecto_supraoseo)]]
        }
        
            input_df = pd.DataFrame(input_data)

            st.session_state.submissions.append(input_df)

            st.write(input_df)

            res = modelo.predict(input_df)

            res = res[0]
            
            c1, c2 = st.columns(2)

            with c1:

                st.markdown("""
                    <style>
                    .big-font {
                    font-size:50px !important;
                    font-weight: bold;
                    }
                    </style>""", unsafe_allow_html=True)
                
                st.markdown(f'<p class="big-font">El tiempo estimado de la intevención es: {res}</p>', unsafe_allow_html=True)

            with c2:
                st.image("verdecirc.jpg", use_column_width="auto", output_format="PNG")


        
surveyMod()