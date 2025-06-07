import re

def extract_metadata(text):
    name_match = re.search(r"(?:Paciente|Nome)[\s:]*([A-ZÀ-Ú][a-zà-ú]+(?: [A-ZÀ-Ú][a-zà-ú]+)+)", text)
    age_match = re.search(r"(?:Idade)[\s:]*([0-9]{1,3})", text)
    modality_match = re.search(r"(hemodi[aá]lise|di[aá]lise peritoneal|di[aá]lise)", text, re.IGNORECASE)

    return {
        "nome": name_match.group(1).strip() if name_match else "Não identificado",
        "idade": age_match.group(1) if age_match else "Não informada",
        "modalidade": modality_match.group(1).capitalize() if modality_match else "Não informada"
    }

def analyze_exam_text(text):
    def extract_value(label, unit):
        pattern = rf"{label}[^\d]*(\d+[\.,]?\d*)[^\d]*{unit}"
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1).replace(",", ".")) if match else None

    results = {
        "hemoglobina": extract_value("hemoglobina", "g/dL"),
        "ferritina": extract_value("ferritina", "ng/mL"),
        "transferrina": extract_value("transferrina", "%"),
        "calcio": extract_value("c[aá]lcio", "mg/dL"),
        "fosforo": extract_value("f[oó]sforo", "mg/dL"),
        "pth": extract_value("pth", "pg/mL"),
        "vitamina_d": extract_value("25.?\s*hidroxi.?vitamina\s*d", "ng/mL"),
    }

    metadata = extract_metadata(text)
    return {"dados": results, "meta": metadata}

def generate_report(parsed):
    values = parsed["dados"]
    meta = parsed["meta"]
    dx = []
    condutas = []

    if values["hemoglobina"] and values["hemoglobina"] < 10:
        dx.append("Anemia da DRC")
        condutas.append("Iniciar alfaepoetina e avaliar ferro sérico.")

    if values["ferritina"] and values["ferritina"] < 100:
        condutas.append("Reposição de ferro (ex: sacarato férrico).")

    if values["pth"] and values["pth"] > 600:
        dx.append("Hiperparatireoidismo secundário")
        condutas.append("Avaliar uso de paricalcitol e/ou cinacalcete.")

    if values["fosforo"] and values["fosforo"] > 5.5:
        condutas.append("Iniciar quelante de fósforo (ex: sevelamer).")

    if values["vitamina_d"] and values["vitamina_d"] < 20:
        condutas.append("Suplementar vitamina D (calcitriol ou colecalciferol).")

    if not dx:
        dx.append("Sem alterações críticas detectadas.")

    texto = f"Paciente: {meta['nome']}\nIdade: {meta['idade']}\nModalidade: {meta['modalidade']}\n"
    texto += "\nDiagnósticos prováveis:\n- " + "\n- ".join(dx)
    texto += "\n\nCondutas sugeridas:\n- " + "\n- ".join(condutas)
    texto += "\n\nEvolução clínica automática:\nPaciente em diálise com alterações laboratoriais compatíveis com " + ", ".join(dx) + ". Seguir PCDT vigente."
    return texto