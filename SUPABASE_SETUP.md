# Configuração do Supabase para PCDT Diálise Assistente

## ✅ Credenciais Já Configuradas

O arquivo `.env` já está configurado com as credenciais do seu projeto Supabase:

- **URL:** https://ddexhfohggodriqdxwzn.supabase.co
- **Projeto:** PCDT

---

## 📋 Passo a Passo para Criar a Tabela

### 1. Acesse o Supabase

1. Vá em https://supabase.com
2. Faça login
3. Selecione o projeto **PCDT** (ou ddexhfohggodriqdxwzn)

### 2. Abra o SQL Editor

1. No menu lateral, clique em **SQL Editor**
2. Clique em **New Query** (Nova Consulta)

### 3. Execute o SQL

Copie e cole o conteúdo do arquivo `supabase_schema.sql` ou copie o SQL abaixo:

```sql
-- Tabela para armazenar relatórios de pacientes em diálise
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

-- Adicionar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_nome ON relatorios_pcdt(nome);
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_data_registro ON relatorios_pcdt(data_registro DESC);
CREATE INDEX IF NOT EXISTS idx_relatorios_pcdt_created_at ON relatorios_pcdt(created_at DESC);
```

4. Clique em **Run** (Executar)
5. Você verá a mensagem "Success. No rows returned"

### 4. Verificar a Tabela

1. No menu lateral, clique em **Table Editor**
2. Você deve ver a tabela `relatorios_pcdt` na lista

---

## 🔐 Estrutura da Tabela

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| **id** | BIGSERIAL | ID único (chave primária) |
| **nome** | TEXT | Nome do paciente |
| **idade** | TEXT | Idade do paciente |
| **modalidade** | TEXT | Tipo de diálise (hemodiálise, peritoneal, etc) |
| **resumo** | TEXT | Resumo dos diagnósticos |
| **conteudo** | TEXT | Relatório completo |
| **data_registro** | TIMESTAMP | Data/hora de geração do relatório |
| **created_at** | TIMESTAMP | Data/hora de criação no banco |

---

## ✅ Como Testar

Depois de criar a tabela, teste o sistema:

1. **Inicie o Streamlit:**
   ```bash
   streamlit run app.py
   ```

2. **Faça upload de um PDF** de exame

3. **Clique em "Analisar Exames"**

4. **Clique em "☁️ Salvar no Supabase"**

5. **Verifique no Supabase:**
   - Vá em **Table Editor** → **relatorios_pcdt**
   - Você deve ver o relatório salvo!

---

## 🔧 Troubleshooting

### Erro: "relation 'relatorios_pcdt' does not exist"

**Solução:** A tabela não foi criada. Execute o SQL no passo 3 acima.

### Erro: "SUPABASE_URL and SUPABASE_KEY must be set"

**Solução:** Verifique se o arquivo `.env` existe e contém as credenciais.

### Erro: "permission denied for table relatorios_pcdt"

**Solução:** Configure as políticas de acesso (Row Level Security):

```sql
-- Permitir inserção para usuários autenticados (ou anônimos para testes)
ALTER TABLE relatorios_pcdt ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable insert for anon users" ON relatorios_pcdt
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Enable read for anon users" ON relatorios_pcdt
    FOR SELECT
    USING (true);
```

---

## 📊 Consultas Úteis

### Ver todos os relatórios

```sql
SELECT * FROM relatorios_pcdt ORDER BY created_at DESC;
```

### Ver relatórios por paciente

```sql
SELECT * FROM relatorios_pcdt
WHERE nome ILIKE '%João%'
ORDER BY data_registro DESC;
```

### Contar relatórios por modalidade

```sql
SELECT modalidade, COUNT(*) as total
FROM relatorios_pcdt
GROUP BY modalidade;
```

### Relatórios dos últimos 7 dias

```sql
SELECT nome, idade, resumo, data_registro
FROM relatorios_pcdt
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
```

---

## 🎯 Próximos Passos (Opcional)

### 1. Adicionar Autenticação

Para proteger os dados, você pode adicionar autenticação de usuários.

### 2. Row Level Security (RLS)

Configure políticas para que cada usuário veja apenas seus próprios relatórios.

### 3. Backup Automático

O Supabase já faz backups automáticos, mas você pode configurar backups adicionais.

---

**Tudo pronto!** Depois de criar a tabela, seu sistema estará totalmente funcional! 🚀
