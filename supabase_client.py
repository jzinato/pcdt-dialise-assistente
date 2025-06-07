from supabase import create_client
import datetime

# Configurações do Supabase (insira as suas)
SUPABASE_URL = "https://bzmjlmddcccbqongzsna.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ6bWpsbWRkY2NjYnFvbmd6c25hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkyOTk3NzksImV4cCI6MjA2NDg3NTc3OX0.UsVRgkuLtJvUBxZynZKjed7U7lUDvFg1SkKqbFgSvsU"

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