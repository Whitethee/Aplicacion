
import markdown
import streamlit as st
from pages.Dashboard import dashboard
from pages.Modelo import surveyMod

st.set_page_config(
    page_title="Software de Predicción Quirúrgica",
    page_icon="👋"
)
st.title("Información")
f = f"""
    <span style="font-weight:bold;">Developer Info and Project Utilities</span>
    """

st.write(f, unsafe_allow_html=True)
st.write("__________________________________________________________________________________")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Descripción")
    st.markdown()


with c2:
    st.subheader("¿Quienes somos?")

