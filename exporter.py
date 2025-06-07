from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def gerar_pdf_relatorio(texto, nome_arquivo="relatorio_pcdt.pdf"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x, y = 40, height - 50

    for linha in texto.split("\n"):
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(x, y, linha)
        y -= 15

    c.save()
    buffer.seek(0)
    return buffer