# Test Fixtures

This directory contains sample data files used in automated tests.

## Files

### `sample_exam_text.txt`
Sample exam text with normal lab values for a dialysis patient. Used to test text extraction and parsing.

## PDF Test Files

For PDF parser tests, you can generate sample PDFs using the following methods:

### Method 1: Using ReportLab (already a project dependency)

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_sample_pdf():
    c = canvas.Canvas("tests/fixtures/sample_valid.pdf", pagesize=A4)
    c.drawString(100, 800, "Paciente: João Silva Santos")
    c.drawString(100, 780, "Idade: 65")
    c.drawString(100, 760, "Hemoglobina: 11.5 g/dL")
    c.save()

create_sample_pdf()
```

### Method 2: Manual Creation
You can also create small PDF files manually and place them in this directory:
- `sample_valid.pdf` - Valid PDF with extractable text
- `sample_empty.pdf` - Valid but empty PDF
- `sample_corrupted.pdf` - Invalid/corrupted PDF for error testing

## Usage in Tests

Fixtures are automatically discovered by pytest via `conftest.py`. Use them in tests like:

```python
def test_example(sample_exam_text_normal):
    result = analyze_exam_text(sample_exam_text_normal)
    assert result is not None
```
