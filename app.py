import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.diagnosis_engine import analyze_exam_text, generate_report
from utils.supabase_client import registrar_relatorio
from utils.exporter import gerar_pdf_relatorio
from utils.docx_exporter import gerar_docx_relatorio

st.set_page_config(page_title="PCDT Diálise Assistente", layout="wide")

st.title("🩺 PCDT Diálise - Diagnóstico Automatizado")

uploaded_file = st.file_uploader("Envie um exame em PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extraindo texto do PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Texto extraído:", text, height=200)

    if st.button("🔍 Analisar e Gerar Diagnóstico"):
        with st.spinner("Analisando resultados..."):
            results = analyze_exam_text(text)
            report = generate_report(results)
            registrar_relatorio(results['meta'], report.split('Evolução clínica')[0], report)
            st.success("Diagnóstico gerado com sucesso!")
            st.text_area("Evolução Clínica e Condutas:", report, height=300)

        if st.download_button("📄 Baixar Relatório em PDF", gerar_pdf_relatorio(report), file_name="relatorio_pcdt.pdf"):
            st.success("PDF gerado com sucesso!")