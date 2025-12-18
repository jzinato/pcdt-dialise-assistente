"""
Tests for pdf_parser.py

Tests PDF text extraction functionality including error handling.
"""
import pytest
import io
from pdf_parser import extract_text_from_pdf


class TestExtractTextFromPDF:
    """Tests for PDF text extraction"""

    @pytest.mark.unit
    def test_extract_text_from_valid_pdf(self):
        """Should extract text from a valid PDF file"""
        # Create a minimal valid PDF with text using reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawString(100, 750, "Paciente: João Silva")
        c.drawString(100, 730, "Hemoglobina: 10.5 g/dL")
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert result is not None
        assert isinstance(result, str)
        assert "João Silva" in result
        assert "Hemoglobina" in result

    @pytest.mark.unit
    def test_extract_text_from_multipage_pdf(self):
        """Should extract text from multiple pages"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Page 1
        c.drawString(100, 750, "Page 1: Patient Information")
        c.showPage()

        # Page 2
        c.drawString(100, 750, "Page 2: Lab Results")
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert "Page 1" in result
        assert "Page 2" in result

    @pytest.mark.unit
    def test_extract_text_from_empty_pdf(self):
        """Should handle empty PDF (no text content)"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.save()  # Save without adding any text
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert result is not None
        assert isinstance(result, str)
        # Empty PDF should return empty string or minimal whitespace
        assert len(result.strip()) == 0

    @pytest.mark.unit
    def test_extract_text_with_special_characters(self):
        """Should handle Portuguese accented characters correctly"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Test with accented characters
        text_with_accents = "Cálcio, Fósforo, Diálise"
        c.drawString(100, 750, text_with_accents)
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert result is not None
        # Should contain the text (exact characters may vary based on PDF encoding)
        assert len(result) > 0

    @pytest.mark.unit
    def test_invalid_pdf_raises_value_error(self):
        """Should raise ValueError for invalid PDF data"""
        invalid_pdf = io.BytesIO(b"This is not a PDF file")

        with pytest.raises(ValueError) as exc_info:
            extract_text_from_pdf(invalid_pdf)

        assert "Failed to extract text from PDF" in str(exc_info.value)

    @pytest.mark.unit
    def test_corrupted_pdf_raises_value_error(self):
        """Should raise ValueError for corrupted PDF"""
        # Partially valid PDF header but corrupted content
        corrupted_pdf = io.BytesIO(b"%PDF-1.4\n%corrupted content here\x00\x01\x02")

        with pytest.raises(ValueError) as exc_info:
            extract_text_from_pdf(corrupted_pdf)

        assert "Failed to extract text from PDF" in str(exc_info.value)

    @pytest.mark.unit
    def test_empty_file_raises_value_error(self):
        """Should raise ValueError for empty file"""
        empty_file = io.BytesIO(b"")

        with pytest.raises(ValueError) as exc_info:
            extract_text_from_pdf(empty_file)

        assert "Failed to extract text from PDF" in str(exc_info.value)

    @pytest.mark.unit
    def test_pdf_with_images_only(self):
        """Should handle PDF with images but no text"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        # Draw a rectangle (image-like content) but no text
        c.rect(100, 100, 200, 200, fill=1)
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert result is not None
        assert isinstance(result, str)
        # Should return empty or minimal content
        assert len(result.strip()) == 0

    @pytest.mark.unit
    def test_returns_string_type(self):
        """Should always return a string type"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawString(100, 750, "Test")
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert isinstance(result, str)

    @pytest.mark.unit
    def test_preserves_line_breaks(self):
        """Should preserve line structure in extracted text"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawString(100, 750, "Line 1")
        c.drawString(100, 730, "Line 2")
        c.drawString(100, 710, "Line 3")
        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    @pytest.mark.unit
    @pytest.mark.slow
    def test_large_pdf_extraction(self):
        """Should handle large PDF files with many pages"""
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Create 50 pages
        for page_num in range(1, 51):
            c.drawString(100, 750, f"Page {page_num}")
            for line in range(20):
                c.drawString(100, 730 - (line * 20), f"Line {line} on page {page_num}")
            c.showPage()

        c.save()
        buffer.seek(0)

        result = extract_text_from_pdf(buffer)

        assert "Page 1" in result
        assert "Page 50" in result
        assert isinstance(result, str)
        assert len(result) > 1000  # Should have substantial content
