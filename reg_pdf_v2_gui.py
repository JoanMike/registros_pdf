import os
import io
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from decimal import Decimal

def add_text_to_pdf(input_pdf_path, output_pdf_path, text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    text_width = Decimal(stringWidth(text, 'Helvetica', 12))
    text_height = 12  # Altura del texto

    existing_pdf = PdfReader(open(input_pdf_path, "rb"))
    page = existing_pdf.pages[0]  # Obtiene la primera página
    page_width = page.mediabox.width
    page_height = page.mediabox.height

    x = page_width - text_width - Decimal(20)  # Resta el ancho del texto y un margen de 20 puntos
    y = page_height - Decimal(10)  # Resta un margen de 10 puntos

    # Dibuja un rectángulo blanco detrás del texto
    can.setFillColorRGB(1, 1, 1)  # Color blanco
    can.setStrokeColorRGB(1, 1, 1)  # Color blanco para el borde
    can.rect(float(x), float(y) - text_height + 10, float(text_width), text_height, fill=1, stroke=1)  # Ajusta la posición y del rectángulo

    # Dibuja el texto
    can.setFillColorRGB(0, 0, 0)  # Color negro
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

def select_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)  # Borra el contenido actual
    directory_entry.insert(0, directory)  # Inserta el directorio seleccionado

def start_processing():
    directory = directory_entry.get()
    process_files(directory)
    print("Proceso terminado.")

root = tk.Tk()

directory_entry = tk.Entry(root)
directory_entry.pack()

select_button = tk.Button(root, text="Seleccionar carpeta", command=select_directory)
select_button.pack()

process_button = tk.Button(root, text="Procesar", command=start_processing)
process_button.pack()

root.mainloop()