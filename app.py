import streamlit as st
from pdf_parser import extract_text_from_pdf
from diagnosis_engine import analyze_exam_text, generate_report
from exporter import gerar_pdf_relatorio
from docx_exporter import gerar_docx_relatorio
from supabase_client import registrar_relatorio

st.title("PCDT Diálise Assistente")
st.markdown("### Sistema de Análise de Exames para Pacientes em Diálise")

uploaded_file = st.file_uploader("Envie o PDF do exame", type="pdf")

if uploaded_file:
    with st.spinner("Extraindo texto do PDF..."):
        texto = extract_text_from_pdf(uploaded_file)

    st.success("✅ Texto extraído com sucesso!")

    with st.expander("📄 Texto extraído do PDF"):
        st.text_area("Conteúdo:", texto, height=300)

    if st.button("🔍 Analisar Exames"):
        with st.spinner("Analisando valores laboratoriais..."):
            resultado = analyze_exam_text(texto)
            relatorio = generate_report(resultado)

        st.success("✅ Análise concluída!")

        # Mostrar metadados do paciente
        st.subheader("👤 Dados do Paciente")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nome", resultado["meta"]["nome"])
        with col2:
            st.metric("Idade", resultado["meta"]["idade"])
        with col3:
            st.metric("Modalidade", resultado["meta"]["modalidade"])

        # Mostrar valores laboratoriais
        st.subheader("🧪 Valores Laboratoriais")
        dados = resultado["dados"]

        col1, col2 = st.columns(2)
        with col1:
            if dados["hemoglobina"]:
                st.metric("Hemoglobina", f"{dados['hemoglobina']} g/dL")
            if dados["ferritina"]:
                st.metric("Ferritina", f"{dados['ferritina']} ng/mL")
            if dados["calcio"]:
                st.metric("Cálcio", f"{dados['calcio']} mg/dL")
            if dados["fosforo"]:
                st.metric("Fósforo", f"{dados['fosforo']} mg/dL")

        with col2:
            if dados["pth"]:
                st.metric("PTH", f"{dados['pth']} pg/mL")
            if dados["vitamina_d"]:
                st.metric("Vitamina D", f"{dados['vitamina_d']} ng/mL")
            if dados["transferrina"]:
                st.metric("Saturação Transferrina", f"{dados['transferrina']} %")

        # Mostrar relatório completo
        st.subheader("📋 Relatório Clínico")
        st.text_area("Relatório Completo", relatorio, height=400)

        # Opções de exportação
        st.subheader("💾 Exportar Relatório")
        col1, col2, col3 = st.columns(3)

        with col1:
            pdf_buffer = gerar_pdf_relatorio(relatorio)
            st.download_button(
                label="📥 Download PDF",
                data=pdf_buffer,
                file_name="relatorio_pcdt.pdf",
                mime="application/pdf"
            )

        with col2:
            docx_buffer = gerar_docx_relatorio(relatorio)
            st.download_button(
                label="📥 Download DOCX",
                data=docx_buffer,
                file_name="relatorio_pcdt.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        with col3:
            if st.button("☁️ Salvar no Supabase"):
                try:
                    # Criar resumo dos diagnósticos
                    linhas_diagnostico = [linha for linha in relatorio.split('\n') if 'Diagnósticos prováveis:' in linha or linha.strip().startswith('-')]
                    resumo = linhas_diagnostico[1] if len(linhas_diagnostico) > 1 else "Relatório gerado"

                    registrar_relatorio(resultado["meta"], resumo.strip('- '), relatorio)
                    st.success("✅ Relatório salvo no banco de dados!")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar: {str(e)}")