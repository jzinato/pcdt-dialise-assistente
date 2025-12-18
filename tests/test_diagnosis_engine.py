"""
Comprehensive tests for diagnosis_engine.py

This module contains critical medical decision logic and requires thorough testing.
Tests are marked with @pytest.mark.critical for high-priority test cases.
"""
import pytest
from diagnosis_engine import extract_metadata, analyze_exam_text, generate_report


class TestExtractMetadata:
    """Tests for patient metadata extraction from text"""

    @pytest.mark.unit
    def test_extract_valid_patient_name(self):
        """Should extract patient name with multiple words"""
        text = "Paciente: João Silva Santos\nIdade: 65"
        result = extract_metadata(text)
        assert result["nome"] == "João Silva Santos"

    @pytest.mark.unit
    def test_extract_patient_name_with_label_nome(self):
        """Should extract patient name using 'Nome' label"""
        text = "Nome: Maria Oliveira Costa\nIdade: 42"
        result = extract_metadata(text)
        assert result["nome"] == "Maria Oliveira Costa"

    @pytest.mark.unit
    def test_extract_patient_name_with_accents(self):
        """Should handle Portuguese accented characters in names"""
        text = "Paciente: José Márcio Araújo\nIdade: 50"
        result = extract_metadata(text)
        assert result["nome"] == "José Márcio Araújo"

    @pytest.mark.unit
    def test_missing_patient_name(self):
        """Should return 'Não identificado' when name is missing"""
        text = "Idade: 50\nExames realizados em 15/03/2024"
        result = extract_metadata(text)
        assert result["nome"] == "Não identificado"

    @pytest.mark.unit
    def test_extract_age_single_digit(self):
        """Should extract single-digit age"""
        text = "Nome: Teste\nIdade: 5"
        result = extract_metadata(text)
        assert result["idade"] == "5"

    @pytest.mark.unit
    def test_extract_age_two_digits(self):
        """Should extract two-digit age"""
        text = "Nome: Teste\nIdade: 65"
        result = extract_metadata(text)
        assert result["idade"] == "65"

    @pytest.mark.unit
    def test_extract_age_three_digits(self):
        """Should extract three-digit age (edge case, but valid)"""
        text = "Nome: Teste\nIdade: 110"
        result = extract_metadata(text)
        assert result["idade"] == "110"

    @pytest.mark.unit
    def test_missing_age(self):
        """Should return 'Não informada' when age is missing"""
        text = "Nome: João Silva\nExames: diversos"
        result = extract_metadata(text)
        assert result["idade"] == "Não informada"

    @pytest.mark.unit
    def test_modality_hemodialise_with_accent(self):
        """Should detect 'hemodiálise' with accent"""
        text = "Paciente em hemodiálise há 3 anos"
        result = extract_metadata(text)
        assert "hemodiálise" in result["modalidade"].lower()

    @pytest.mark.unit
    def test_modality_hemodialise_without_accent(self):
        """Should detect 'hemodialise' without accent"""
        text = "Paciente em hemodialise há 3 anos"
        result = extract_metadata(text)
        assert "hemodialise" in result["modalidade"].lower()

    @pytest.mark.unit
    def test_modality_peritoneal_dialysis(self):
        """Should detect 'diálise peritoneal'"""
        text = "Tratamento: diálise peritoneal"
        result = extract_metadata(text)
        assert "peritoneal" in result["modalidade"].lower()

    @pytest.mark.unit
    def test_modality_generic_dialise(self):
        """Should detect generic 'diálise'"""
        text = "Paciente em diálise"
        result = extract_metadata(text)
        assert "diálise" in result["modalidade"].lower()

    @pytest.mark.unit
    def test_missing_modality(self):
        """Should return 'Não informada' when modality is missing"""
        text = "Nome: João\nIdade: 50\nExames diversos"
        result = extract_metadata(text)
        assert result["modalidade"] == "Não informada"


class TestAnalyzeExamText:
    """Tests for lab value extraction from exam text"""

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_hemoglobina_period_decimal(self):
        """Should extract hemoglobin with period as decimal separator"""
        text = "Hemoglobina: 11.5 g/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["hemoglobina"] == 11.5

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_hemoglobina_comma_decimal(self):
        """Should extract hemoglobin with comma as decimal separator"""
        text = "Hemoglobina: 9,5 g/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["hemoglobina"] == 9.5

    @pytest.mark.unit
    def test_extract_hemoglobina_integer(self):
        """Should extract hemoglobin as integer value"""
        text = "Hemoglobina: 10 g/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["hemoglobina"] == 10.0

    @pytest.mark.unit
    def test_extract_hemoglobina_case_insensitive(self):
        """Should extract hemoglobin regardless of case"""
        text = "HEMOGLOBINA: 12.5 g/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["hemoglobina"] == 12.5

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_ferritina(self):
        """Should extract ferritin value"""
        text = "Ferritina: 250.5 ng/mL"
        result = analyze_exam_text(text)
        assert result["dados"]["ferritina"] == 250.5

    @pytest.mark.unit
    def test_extract_ferritina_comma_decimal(self):
        """Should extract ferritin with comma decimal"""
        text = "Ferritina: 120,5 ng/mL"
        result = analyze_exam_text(text)
        assert result["dados"]["ferritina"] == 120.5

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_transferrina(self):
        """Should extract transferrin saturation"""
        text = "Saturação de Transferrina: 35.8 %"
        result = analyze_exam_text(text)
        assert result["dados"]["transferrina"] == 35.8

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_calcio_with_accent(self):
        """Should extract calcium with accent (cálcio)"""
        text = "Cálcio: 9.2 mg/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["calcio"] == 9.2

    @pytest.mark.unit
    def test_extract_calcio_without_accent(self):
        """Should extract calcium without accent (calcio)"""
        text = "Calcio: 8.5 mg/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["calcio"] == 8.5

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_fosforo_with_accent(self):
        """Should extract phosphorus with accent (fósforo)"""
        text = "Fósforo: 5.6 mg/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["fosforo"] == 5.6

    @pytest.mark.unit
    def test_extract_fosforo_without_accent(self):
        """Should extract phosphorus without accent (fosforo)"""
        text = "Fosforo: 6.2 mg/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["fosforo"] == 6.2

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_pth(self):
        """Should extract PTH (parathyroid hormone)"""
        text = "PTH: 450.3 pg/mL"
        result = analyze_exam_text(text)
        assert result["dados"]["pth"] == 450.3

    @pytest.mark.unit
    @pytest.mark.critical
    def test_extract_vitamina_d(self):
        """Should extract 25-hydroxyvitamin D"""
        text = "25-hidroxivitamina D: 28.5 ng/mL"
        result = analyze_exam_text(text)
        assert result["dados"]["vitamina_d"] == 28.5

    @pytest.mark.unit
    def test_extract_vitamina_d_various_formats(self):
        """Should extract vitamin D with various formatting"""
        text = "25 hidroxi vitamina D: 22 ng/mL"
        result = analyze_exam_text(text)
        assert result["dados"]["vitamina_d"] == 22.0

    @pytest.mark.unit
    def test_missing_value_returns_none(self):
        """Should return None for missing values"""
        text = "Hemoglobina: 10 g/dL\nCalcio: 9 mg/dL"
        result = analyze_exam_text(text)
        assert result["dados"]["pth"] is None
        assert result["dados"]["ferritina"] is None

    @pytest.mark.unit
    def test_includes_metadata(self):
        """Should include patient metadata in results"""
        text = "Paciente: João Silva\nIdade: 65\nHemoglobina: 10 g/dL"
        result = analyze_exam_text(text)
        assert "meta" in result
        assert result["meta"]["nome"] == "João Silva"
        assert result["meta"]["idade"] == "65"

    @pytest.mark.unit
    def test_all_values_extractable(self, sample_exam_text_normal):
        """Should extract all lab values from complete exam text"""
        result = analyze_exam_text(sample_exam_text_normal)
        dados = result["dados"]

        assert dados["hemoglobina"] is not None
        assert dados["ferritina"] is not None
        assert dados["transferrina"] is not None
        assert dados["calcio"] is not None
        assert dados["fosforo"] is not None
        assert dados["pth"] is not None
        assert dados["vitamina_d"] is not None


class TestGenerateReport:
    """Tests for clinical report generation based on lab values"""

    @pytest.mark.unit
    @pytest.mark.critical
    def test_anemia_diagnosis_below_threshold(self):
        """Should diagnose anemia when hemoglobin < 10 g/dL"""
        parsed = {
            "dados": {
                "hemoglobina": 9.0,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test Patient", "idade": "60", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Anemia da DRC" in report
        assert "alfaepoetina" in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_hemoglobina_at_boundary_10(self):
        """Should NOT diagnose anemia at exactly 10.0 g/dL (boundary test)"""
        parsed = {
            "dados": {
                "hemoglobina": 10.0,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Anemia da DRC" not in report
        assert "alfaepoetina" not in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_hemoglobina_just_below_threshold(self):
        """Should diagnose anemia at 9.9 g/dL (just below threshold)"""
        parsed = {
            "dados": {
                "hemoglobina": 9.9,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Anemia da DRC" in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_ferritina_below_threshold(self):
        """Should recommend iron replacement when ferritin < 100 ng/mL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": 80.0,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "ferro" in report.lower()
        assert "sacarato" in report.lower()

    @pytest.mark.unit
    @pytest.mark.critical
    def test_ferritina_at_boundary_100(self):
        """Should NOT recommend iron at exactly 100 ng/mL (boundary test)"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": 100.0,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        # Should not recommend iron at exactly 100
        assert "sacarato férrico" not in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_pth_hyperparathyroidism_above_threshold(self):
        """Should diagnose secondary hyperparathyroidism when PTH > 600 pg/mL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": 700.0,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Hiperparatireoidismo secundário" in report
        assert "paricalcitol" in report or "cinacalcete" in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_pth_at_boundary_600(self):
        """Should NOT diagnose hyperparathyroidism at exactly 600 pg/mL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": 600.0,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Hiperparatireoidismo secundário" not in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_fosforo_above_threshold(self):
        """Should recommend phosphate binder when phosphorus > 5.5 mg/dL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": 6.0,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "fósforo" in report.lower()
        assert "sevelamer" in report.lower()

    @pytest.mark.unit
    @pytest.mark.critical
    def test_fosforo_at_boundary_5_5(self):
        """Should NOT recommend phosphate binder at exactly 5.5 mg/dL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": 5.5,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "sevelamer" not in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_vitamina_d_below_threshold(self):
        """Should recommend vitamin D supplementation when < 20 ng/mL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": 15.0
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "vitamina D" in report
        assert "calcitriol" in report or "colecalciferol" in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_vitamina_d_at_boundary_20(self):
        """Should NOT recommend vitamin D at exactly 20 ng/mL"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": 20.0
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Suplementar vitamina D" not in report

    @pytest.mark.unit
    def test_no_abnormalities(self, sample_parsed_data_normal):
        """Should report no critical alterations for normal values"""
        report = generate_report(sample_parsed_data_normal)
        assert "Sem alterações críticas detectadas" in report

    @pytest.mark.unit
    @pytest.mark.critical
    def test_multiple_conditions_simultaneously(self):
        """Should handle multiple abnormal conditions in one report"""
        parsed = {
            "dados": {
                "hemoglobina": 8.0,
                "ferritina": 70.0,
                "transferrina": None,
                "calcio": None,
                "fosforo": 6.5,
                "pth": 750.0,
                "vitamina_d": 12.0
            },
            "meta": {"nome": "Complex Case", "idade": "65", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)

        # All conditions should be present
        assert "Anemia da DRC" in report
        assert "Hiperparatireoidismo" in report
        assert "alfaepoetina" in report
        assert "ferro" in report
        assert "fósforo" in report
        assert "vitamina D" in report

    @pytest.mark.unit
    def test_report_includes_patient_metadata(self):
        """Should include patient name, age, and modality in report"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {
                "nome": "João Silva Santos",
                "idade": "65",
                "modalidade": "Hemodiálise"
            }
        }
        report = generate_report(parsed)
        assert "João Silva Santos" in report
        assert "65" in report
        assert "Hemodiálise" in report

    @pytest.mark.unit
    def test_report_structure(self):
        """Should have proper report structure with sections"""
        parsed = {
            "dados": {
                "hemoglobina": 9.0,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "60", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)

        assert "Paciente:" in report
        assert "Idade:" in report
        assert "Modalidade:" in report
        assert "Diagnósticos prováveis:" in report
        assert "Condutas sugeridas:" in report
        assert "Evolução clínica automática:" in report

    @pytest.mark.unit
    def test_none_values_handled_safely(self):
        """Should handle all None values without errors"""
        parsed = {
            "dados": {
                "hemoglobina": None,
                "ferritina": None,
                "transferrina": None,
                "calcio": None,
                "fosforo": None,
                "pth": None,
                "vitamina_d": None
            },
            "meta": {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        }
        report = generate_report(parsed)
        assert "Sem alterações críticas detectadas" in report
        assert report is not None
        assert len(report) > 0
