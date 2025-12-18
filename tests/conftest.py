"""
Shared fixtures and configuration for pytest
"""
import pytest
import io


@pytest.fixture
def sample_exam_text_normal():
    """Sample exam text with normal values"""
    return """
    Paciente: João Silva Santos
    Idade: 65
    Modalidade: Hemodiálise

    Resultados dos Exames:
    Hemoglobina: 11.5 g/dL
    Ferritina: 250 ng/mL
    Saturação de Transferrina: 35 %
    Cálcio: 9.2 mg/dL
    Fósforo: 4.8 mg/dL
    PTH: 350 pg/mL
    25-hidroxivitamina D: 28 ng/mL
    """


@pytest.fixture
def sample_exam_text_anemia():
    """Sample exam text with anemia (hemoglobin < 10)"""
    return """
    Paciente: Maria Oliveira Costa
    Idade: 58
    Modalidade: Diálise Peritoneal

    Resultados dos Exames:
    Hemoglobina: 8.5 g/dL
    Ferritina: 80 ng/mL
    Saturação de Transferrina: 18 %
    Cálcio: 9.0 mg/dL
    Fósforo: 5.2 mg/dL
    PTH: 450 pg/mL
    25-hidroxivitamina D: 22 ng/mL
    """


@pytest.fixture
def sample_exam_text_hyperparathyroidism():
    """Sample exam text with secondary hyperparathyroidism (PTH > 600)"""
    return """
    Paciente: Carlos Eduardo Souza
    Idade: 72
    Modalidade: Hemodiálise

    Resultados dos Exames:
    Hemoglobina: 10.2 g/dL
    Ferritina: 180 ng/mL
    Saturação de Transferrina: 28 %
    Cálcio: 8.5 mg/dL
    Fósforo: 6.8 mg/dL
    PTH: 850 pg/mL
    25-hidroxivitamina D: 15 ng/mL
    """


@pytest.fixture
def sample_exam_text_multiple_conditions():
    """Sample exam text with multiple abnormal conditions"""
    return """
    Paciente: Ana Paula Fernandes
    Idade: 61
    Modalidade: Hemodiálise

    Resultados dos Exames:
    Hemoglobina: 7.8 g/dL
    Ferritina: 65 ng/mL
    Saturação de Transferrina: 15 %
    Cálcio: 8.2 mg/dL
    Fósforo: 7.2 mg/dL
    PTH: 720 pg/mL
    25-hidroxivitamina D: 12 ng/mL
    """


@pytest.fixture
def sample_exam_text_comma_decimals():
    """Sample exam text using comma as decimal separator"""
    return """
    Paciente: Roberto Lima
    Idade: 55
    Modalidade: Hemodiálise

    Resultados dos Exames:
    Hemoglobina: 9,2 g/dL
    Ferritina: 120,5 ng/mL
    Saturação de Transferrina: 22,8 %
    Cálcio: 8,9 mg/dL
    Fósforo: 5,6 mg/dL
    PTH: 580,3 pg/mL
    25-hidroxivitamina D: 18,5 ng/mL
    """


@pytest.fixture
def sample_exam_text_missing_metadata():
    """Sample exam text with missing patient metadata"""
    return """
    Resultados dos Exames de Laboratório

    Hemoglobina: 10.5 g/dL
    Ferritina: 150 ng/mL
    PTH: 400 pg/mL
    """


@pytest.fixture
def sample_exam_text_no_values():
    """Sample exam text with no extractable lab values"""
    return """
    Paciente: José Santos
    Idade: 60
    Modalidade: Diálise

    Exames solicitados mas resultados não disponíveis.
    Aguardando processamento do laboratório.
    """


@pytest.fixture
def mock_pdf_bytes():
    """Mock PDF file as bytes"""
    return io.BytesIO(b"%PDF-1.4\n%mock pdf content")


@pytest.fixture
def sample_report_metadata():
    """Sample patient metadata for reports"""
    return {
        "nome": "João Silva Santos",
        "idade": "65",
        "modalidade": "Hemodiálise"
    }


@pytest.fixture
def sample_parsed_data_normal():
    """Sample parsed data with normal values"""
    return {
        "dados": {
            "hemoglobina": 11.5,
            "ferritina": 250.0,
            "transferrina": 35.0,
            "calcio": 9.2,
            "fosforo": 4.8,
            "pth": 350.0,
            "vitamina_d": 28.0
        },
        "meta": {
            "nome": "João Silva Santos",
            "idade": "65",
            "modalidade": "Hemodiálise"
        }
    }


@pytest.fixture
def sample_parsed_data_anemia():
    """Sample parsed data with anemia"""
    return {
        "dados": {
            "hemoglobina": 8.5,
            "ferritina": 80.0,
            "transferrina": 18.0,
            "calcio": 9.0,
            "fosforo": 5.2,
            "pth": 450.0,
            "vitamina_d": 22.0
        },
        "meta": {
            "nome": "Maria Oliveira Costa",
            "idade": "58",
            "modalidade": "Diálise Peritoneal"
        }
    }
