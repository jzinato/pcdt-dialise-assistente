"""
Tests for supabase_client.py

Tests database operations with mocking to avoid real database calls.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import datetime


class TestRegistrarRelatorio:
    """Tests for registering reports to Supabase"""

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_success(self, mock_supabase):
        """Should successfully register a report to database"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Test data
        meta = {
            "nome": "João Silva",
            "idade": "65",
            "modalidade": "Hemodiálise"
        }
        resumo = "Anemia da DRC"
        texto = "Relatório completo do paciente..."

        # Execute
        registrar_relatorio(meta, resumo, texto)

        # Verify
        mock_supabase.table.assert_called_once_with("relatorios_pcdt")
        assert mock_table.insert.called
        assert mock_insert.execute.called

        # Check the data that was inserted
        call_args = mock_table.insert.call_args[0][0]
        assert call_args["nome"] == "João Silva"
        assert call_args["idade"] == "65"
        assert call_args["modalidade"] == "Hemodiálise"
        assert call_args["resumo"] == resumo
        assert call_args["conteudo"] == texto
        assert "data_registro" in call_args

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_with_datetime(self, mock_supabase):
        """Should include ISO format datetime in registration"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Test data
        meta = {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}

        # Execute
        registrar_relatorio(meta, "Summary", "Full text")

        # Verify datetime is in ISO format
        call_args = mock_table.insert.call_args[0][0]
        assert "data_registro" in call_args

        # Should be a valid ISO format datetime string
        datetime_str = call_args["data_registro"]
        assert isinstance(datetime_str, str)
        # Should be parseable back to datetime
        parsed = datetime.datetime.fromisoformat(datetime_str)
        assert parsed is not None

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_missing_metadata_fields(self, mock_supabase):
        """Should handle missing metadata fields gracefully"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Test data with missing fields
        meta = {"nome": "João Silva"}  # Missing idade and modalidade

        # Execute
        registrar_relatorio(meta, "Summary", "Text")

        # Verify - should use .get() which returns None for missing keys
        call_args = mock_table.insert.call_args[0][0]
        assert call_args["nome"] == "João Silva"
        assert call_args["idade"] is None
        assert call_args["modalidade"] is None

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_empty_metadata(self, mock_supabase):
        """Should handle completely empty metadata dict"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Execute with empty meta
        registrar_relatorio({}, "Summary", "Text")

        # Verify all fields are None
        call_args = mock_table.insert.call_args[0][0]
        assert call_args["nome"] is None
        assert call_args["idade"] is None
        assert call_args["modalidade"] is None
        assert call_args["resumo"] == "Summary"
        assert call_args["conteudo"] == "Text"

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_calls_correct_table(self, mock_supabase):
        """Should call the correct Supabase table"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Execute
        meta = {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        registrar_relatorio(meta, "Summary", "Text")

        # Verify correct table name
        mock_supabase.table.assert_called_once_with("relatorios_pcdt")

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_database_error(self, mock_supabase):
        """Should propagate database errors"""
        from supabase_client import registrar_relatorio

        # Setup mock to raise an error
        mock_table = Mock()
        mock_insert = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.side_effect = Exception("Database connection failed")

        # Execute and expect error
        meta = {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}

        with pytest.raises(Exception) as exc_info:
            registrar_relatorio(meta, "Summary", "Text")

        assert "Database connection failed" in str(exc_info.value)

    @pytest.mark.unit
    @pytest.mark.security
    def test_supabase_client_initialization(self):
        """Should verify Supabase client is properly initialized"""
        import supabase_client

        # Client should exist
        assert hasattr(supabase_client, 'supabase')
        assert supabase_client.supabase is not None

        # Note: In production, credentials should come from environment variables
        # This is a known security issue that should be fixed

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_preserves_special_characters(self, mock_supabase):
        """Should preserve Portuguese special characters in text"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Test with accented characters
        meta = {
            "nome": "José Márcio Araújo",
            "idade": "65",
            "modalidade": "Diálise Peritoneal"
        }
        resumo = "Anemia da DRC, Hiperparatireoidismo"
        texto = "Cálcio: 8.5 mg/dL\nFósforo: 6.2 mg/dL"

        # Execute
        registrar_relatorio(meta, resumo, texto)

        # Verify special characters are preserved
        call_args = mock_table.insert.call_args[0][0]
        assert "José Márcio Araújo" in call_args["nome"]
        assert "Diálise Peritoneal" in call_args["modalidade"]
        assert "Fósforo" in call_args["conteudo"]

    @pytest.mark.unit
    @patch('supabase_client.supabase')
    def test_registrar_relatorio_with_long_text(self, mock_supabase):
        """Should handle long report text"""
        from supabase_client import registrar_relatorio

        # Setup mock
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute

        # Generate long text
        meta = {"nome": "Test", "idade": "50", "modalidade": "Hemodiálise"}
        long_text = "Line of text. " * 1000  # ~14KB of text

        # Execute
        registrar_relatorio(meta, "Summary", long_text)

        # Verify
        call_args = mock_table.insert.call_args[0][0]
        assert len(call_args["conteudo"]) > 10000
        assert call_args["conteudo"] == long_text
