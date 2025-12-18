# Testing Documentation

## Overview

This document describes the test infrastructure for the PCDT Diálise Assistente project. Comprehensive test coverage has been implemented to ensure the reliability and correctness of the clinical decision support system.

## Test Coverage Summary

| Module | Test File | Test Count | Priority | Coverage Target |
|--------|-----------|------------|----------|-----------------|
| `diagnosis_engine.py` | `test_diagnosis_engine.py` | 50+ tests | **P0 - Critical** | 95%+ |
| `pdf_parser.py` | `test_pdf_parser.py` | 12 tests | **P0 - Critical** | 90%+ |
| `supabase_client.py` | `test_supabase_client.py` | 10 tests | **P1 - High** | 85%+ |
| `exporter.py` | `test_exporter.py` | 14 tests | **P2 - Medium** | 80%+ |
| `docx_exporter.py` | `test_docx_exporter.py` | 13 tests | **P3 - Low** | 80%+ |

**Total Tests:** 100+ comprehensive test cases

## Quick Start

### 1. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development/testing dependencies
pip install -r requirements-dev.txt
```

### 2. Configure Environment

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your Supabase credentials
# SUPABASE_URL=your_url_here
# SUPABASE_KEY=your_key_here
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/test_diagnosis_engine.py

# Run tests with specific marker
pytest -m critical      # Only critical tests
pytest -m unit          # Only unit tests
pytest -m security      # Only security tests

# Run with verbose output
pytest -v

# Run and show which tests are slowest
pytest --durations=10
```

## Test Organization

### Directory Structure

```
tests/
├── __init__.py                    # Test package init
├── conftest.py                    # Shared fixtures and configuration
├── fixtures/                      # Test data files
│   ├── sample_exam_text.txt      # Sample exam text
│   └── README.md                 # Fixture documentation
├── test_diagnosis_engine.py      # Tests for core diagnostic logic
├── test_pdf_parser.py            # Tests for PDF extraction
├── test_supabase_client.py       # Tests for database operations (mocked)
├── test_exporter.py              # Tests for PDF report generation
└── test_docx_exporter.py         # Tests for DOCX report generation
```

### Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests for individual functions
- `@pytest.mark.integration` - Integration tests for module interactions
- `@pytest.mark.critical` - Tests for critical medical decision logic
- `@pytest.mark.security` - Security-related tests
- `@pytest.mark.slow` - Tests that take significant time to run

## Critical Test Cases

### Medical Decision Logic (`diagnosis_engine.py`)

The most critical tests validate clinical decision thresholds:

**Anemia Detection:**
- Hemoglobin < 10 g/dL → Diagnose "Anemia da DRC" + recommend erythropoietin
- Boundary test: Exactly 10.0 should NOT trigger diagnosis

**Hyperparathyroidism:**
- PTH > 600 pg/mL → Diagnose "Hiperparatireoidismo secundário"
- Boundary test: Exactly 600.0 should NOT trigger diagnosis

**Iron Deficiency:**
- Ferritin < 100 ng/mL → Recommend iron replacement

**Hyperphosphatemia:**
- Phosphorus > 5.5 mg/dL → Recommend phosphate binders

**Vitamin D Deficiency:**
- 25-OH Vitamin D < 20 ng/mL → Recommend supplementation

All boundary conditions are explicitly tested to ensure correct threshold logic.

### Value Extraction

Tests validate that lab values are correctly extracted from text with:
- Decimal separators (comma vs period): "9,5" vs "9.5"
- Case insensitivity
- Accented characters: "Cálcio" vs "Calcio"
- Missing values (return None)

### PDF Parsing

Tests cover:
- Valid PDF extraction
- Invalid/corrupted PDF error handling
- Empty PDFs
- Multi-page documents
- Special characters

## Running Specific Test Suites

```bash
# Critical medical logic only
pytest -m critical

# All diagnosis engine tests
pytest tests/test_diagnosis_engine.py -v

# Specific test class
pytest tests/test_diagnosis_engine.py::TestGenerateReport -v

# Specific test function
pytest tests/test_diagnosis_engine.py::TestGenerateReport::test_anemia_diagnosis_below_threshold -v

# Skip slow tests
pytest -m "not slow"
```

## Coverage Reports

### Generate HTML Coverage Report

```bash
pytest --cov --cov-report=html
# Open htmlcov/index.html in browser
```

### Generate Terminal Coverage Report

```bash
pytest --cov --cov-report=term-missing
```

### Coverage Goals

- **Immediate (Current):** 70% overall coverage
- **Short-term (1 month):** 85% overall coverage
- **Long-term (3 months):** 90%+ overall coverage

## Continuous Integration

### GitHub Actions (Recommended)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: pytest --cov --cov-fail-under=70
```

## Security Testing

### Credentials Security

- ✅ Credentials moved to environment variables (`.env` file)
- ✅ `.env` excluded from git via `.gitignore`
- ✅ `.env.example` provided as template
- ✅ Application validates credentials are present

### Security Scanning

```bash
# Scan for security issues in code
bandit -r . -x tests/

# Check for vulnerable dependencies
safety check

# Type checking
mypy diagnosis_engine.py pdf_parser.py
```

## Mocking Strategy

### Supabase Client

All database tests use mocking to avoid real database calls:

```python
@patch('supabase_client.supabase')
def test_example(mock_supabase):
    # Setup mock behavior
    mock_supabase.table.return_value.insert.return_value.execute.return_value = {}

    # Test function
    registrar_relatorio(meta, resumo, texto)

    # Verify
    assert mock_supabase.table.called
```

## Test Fixtures

Shared test data is defined in `tests/conftest.py`:

- `sample_exam_text_normal` - Normal lab values
- `sample_exam_text_anemia` - Anemic patient
- `sample_exam_text_hyperparathyroidism` - High PTH
- `sample_exam_text_multiple_conditions` - Multiple abnormalities
- `sample_exam_text_comma_decimals` - Comma decimal separators

## Troubleshooting

### Tests Fail with "SUPABASE_URL not set"

Make sure you've created `.env` file with credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

For tests, you can also mock the environment:

```bash
export SUPABASE_URL="https://test.supabase.co"
export SUPABASE_KEY="test-key"
pytest
```

### Import Errors

Ensure you're running from the project root:

```bash
cd /path/to/pcdt-dialise-assistente
pytest
```

### Coverage Too Low

Check which files/lines aren't covered:

```bash
pytest --cov --cov-report=term-missing
```

## Best Practices

1. **Run tests before committing**
   ```bash
   pytest
   ```

2. **Write tests for new features**
   - Add tests before implementing features (TDD)
   - Ensure >80% coverage for new code

3. **Test boundary conditions**
   - Always test exact threshold values
   - Test just above and just below thresholds

4. **Use descriptive test names**
   - `test_anemia_diagnosis_below_threshold` ✅
   - `test_case_1` ❌

5. **Mark critical tests**
   - Use `@pytest.mark.critical` for medical decision logic

## Further Reading

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)

## Questions?

If you have questions about the test infrastructure, please open an issue on GitHub.
