"""
Tests for exporter.py

Tests PDF report generation functionality.
"""
import pytest
import io
from exporter import gerar_pdf_relatorio


class TestGerarPdfRelatorio:
    """Tests for PDF report generation"""

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_returns_buffer(self):
        """Should return a BytesIO buffer"""
        texto = "Paciente: João Silva\nIdade: 65\nDiagnóstico: Anemia da DRC"
        result = gerar_pdf_relatorio(texto)

        assert isinstance(result, io.BytesIO)
        assert result.tell() == 0  # Buffer should be at position 0

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_creates_valid_pdf(self):
        """Should create a valid PDF file"""
        texto = "Paciente: João Silva\nIdade: 65"
        result = gerar_pdf_relatorio(texto)

        # Read the buffer content
        pdf_content = result.read()

        # Valid PDFs start with %PDF header
        assert pdf_content.startswith(b'%PDF-')
        assert len(pdf_content) > 0

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_with_simple_text(self):
        """Should generate PDF with simple text"""
        texto = "Test Report"
        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert len(pdf_content) > 100  # Should have meaningful content

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_with_multiline_text(self):
        """Should handle multiple lines of text"""
        texto = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_empty_text(self):
        """Should handle empty text"""
        texto = ""
        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_with_long_text(self):
        """Should handle long text requiring multiple pages"""
        # Create text with 100 lines to trigger pagination
        lines = [f"Line {i}: Patient data and exam results" for i in range(100)]
        texto = "\n".join(lines)

        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')
        # Longer text should create larger PDF
        assert len(pdf_content) > 1000

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_pagination(self):
        """Should create multiple pages for long content"""
        # Each line takes ~15 pixels, page height check is at y < 50
        # So approximately (800 - 50) / 15 = 50 lines per page
        # Create 120 lines to ensure multiple pages
        lines = [f"Line {i}" for i in range(120)]
        texto = "\n".join(lines)

        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()

        # Multiple pages should create a larger PDF
        assert len(pdf_content) > 2000

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_with_special_characters(self):
        """Should handle Portuguese special characters"""
        texto = "Paciente: José Márcio\nCálcio: 9.2 mg/dL\nFósforo: 5.5 mg/dL"
        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_default_filename(self):
        """Should accept default filename parameter"""
        texto = "Test"
        result = gerar_pdf_relatorio(texto)

        # Function should work with default filename
        assert result is not None

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_custom_filename(self):
        """Should accept custom filename parameter"""
        texto = "Test"
        custom_name = "custom_report.pdf"
        result = gerar_pdf_relatorio(texto, nome_arquivo=custom_name)

        # Function should work with custom filename
        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_buffer_position(self):
        """Should reset buffer position to start"""
        texto = "Paciente: Test\nResultados: Normal"
        result = gerar_pdf_relatorio(texto)

        # Buffer should be at position 0 for immediate reading
        assert result.tell() == 0

        # Should be readable
        content = result.read()
        assert len(content) > 0

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_complete_report(self):
        """Should generate PDF for a complete clinical report"""
        texto = """Paciente: João Silva Santos
Idade: 65
Modalidade: Hemodiálise

Diagnósticos prováveis:
- Anemia da DRC
- Hiperparatireoidismo secundário

Condutas sugeridas:
- Iniciar alfaepoetina e avaliar ferro sérico.
- Reposição de ferro (ex: sacarato férrico).
- Avaliar uso de paricalcitol e/ou cinacalcete.

Evolução clínica automática:
Paciente em diálise com alterações laboratoriais compatíveis."""

        result = gerar_pdf_relatorio(texto)

        assert result is not None
        pdf_content = result.read()
        assert pdf_content.startswith(b'%PDF-')
        # Complete report should have substantial size
        assert len(pdf_content) > 500

    @pytest.mark.unit
    def test_gerar_pdf_relatorio_returns_new_buffer_each_time(self):
        """Should return a new buffer for each call"""
        texto = "Test"

        result1 = gerar_pdf_relatorio(texto)
        result2 = gerar_pdf_relatorio(texto)

        # Should be different buffer objects
        assert result1 is not result2
        assert id(result1) != id(result2)
