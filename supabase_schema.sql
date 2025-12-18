-- Tabela para armazenar relatórios de pacientes em diálise
-- Execute este SQL no Supabase SQL Editor

CREATE TABLE IF NOT EXISTS relatorios_pcdt (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT,
    idade TEXT,
    modalidade TEXT,
    resumo TEXT,
    conteudo TEXT,
    data_registro TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adicionar índices para melhorar performance de consultas
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_nome ON relatorios_pcdt(nome);
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_data_registro ON relatorios_pcdt(data_registro DESC);
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_created_at ON relatorios_pcdt(created_at DESC);

-- Adicionar comentários para documentação
COMMENT ON TABLE relatorios_pcdt IS 'Armazena relatórios clínicos gerados pelo sistema PCDT Diálise Assistente';
COMMENT ON COLUMN relatorios_pcdt.nome IS 'Nome do paciente extraído do exame';
COMMENT ON COLUMN relatorios_pcdt.idade IS 'Idade do paciente';
COMMENT ON COLUMN relatorios_pcdt.modalidade IS 'Modalidade de diálise (hemodiálise, diálise peritoneal, etc)';
COMMENT ON COLUMN relatorios_pcdt.resumo IS 'Resumo dos diagnósticos principais';
COMMENT ON COLUMN relatorios_pcdt.conteudo IS 'Relatório completo com diagnósticos e condutas';
COMMENT ON COLUMN relatorios_pcdt.data_registro IS 'Data/hora em que o relatório foi gerado pelo sistema';
COMMENT ON COLUMN relatorios_pcdt.created_at IS 'Data/hora em que o registro foi criado no banco de dados';
