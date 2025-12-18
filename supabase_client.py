from supabase import create_client
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurações do Supabase - agora usando variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
        "Copy .env.example to .env and fill in your credentials."
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def registrar_relatorio(meta, resumo, texto):
    data = {
        "nome": meta.get("nome"),
        "idade": meta.get("idade"),
        "modalidade": meta.get("modalidade"),
        "resumo": resumo,
        "conteudo": texto,
        "data_registro": datetime.datetime.now().isoformat()
    }
    supabase.table("relatorios_pcdt").insert(data).execute()