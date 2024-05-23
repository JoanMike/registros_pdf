import os
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from decimal import Decimal

def add_text_to_pdf(input_pdf_path, output_pdf_path, text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    text_width = Decimal(stringWidth(text, 'Helvetica', 12))

    existing_pdf = PdfReader(open(input_pdf_path, "rb"))
    page = existing_pdf.pages[0]  # Obtiene la primera página
    page_width = page.mediabox.width
    page_height = page.mediabox.height

    x = page_width - text_width - Decimal(15)  # Resta el ancho del texto y un margen de 10 puntos
    y = page_height - Decimal(10)  # Resta un margen de 10 puntos

    can.drawString(float(x), float(y), text)
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(input_pdf_path, "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    for page_num in range(1, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[page_num])

    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(directory, filename)
            output_pdf_path = input_pdf_path  # Sobreescribe el archivo original
            text = filename[:10]
            add_text_to_pdf(input_pdf_path, output_pdf_path, text)

# Reemplaza 'my_directory' con la ruta de tu directorio
process_files("C:\\AUTOM\\SPU")