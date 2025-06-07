import streamlit as st
from utils.pdf_parser import extract_text_from_pdf

st.title("PCDT Diálise Assistente")

uploaded_file = st.file_uploader("Envie o PDF do exame", type="pdf")
if uploaded_file:
    texto = extract_text_from_pdf(uploaded_file)
    st.text_area("Texto extraído:", texto, height=300)