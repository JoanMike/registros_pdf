import os
import fitz  # PyMuPDF
import shutil  # Para operaciones con archivos

def agregar_texto_a_pdf(ruta_carpeta):
    # Lista todos los archivos en la carpeta
    archivos = os.listdir(ruta_carpeta)

    for archivo in archivos:
        if archivo.endswith('.pdf'):
            try:
                # Obtiene los primeros 10 caracteres del nombre del archivo
                texto = archivo[:10]

                # Abre el archivo PDF
                doc = fitz.open(os.path.join(ruta_carpeta, archivo))

                # Selecciona la primera página
                pagina = doc[0]

                # Define las propiedades del texto
                color = (0, 0, 0)  # Color del texto en RGB, rojo para mayor visibilidad
                fuente = 'helv'  # Fuente Helvetica
                tamano = 12  # Tamaño de la fuente

                # Obtiene las dimensiones de la hoja
                ancho, alto = pagina.rect.width, pagina.rect.height

                # Define la ubicación del texto en la esquina superior derecha
                # ajustando las coordenadas en función del tamaño de la hoja
                x1 = ancho - 150  # 150 es la distancia desde la esquina derecha
                y1 = alto - 50  # 50 es la distancia desde la esquina superior
                x2 = ancho - 10  # 10 es el margen derecho
                y2 = alto - 10  # 10 es el margen superior
                ubicacion = fitz.Rect(x1, y1, x2, y2)

                # Agrega el texto a la página
                pagina.insert_textbox(ubicacion, texto, fontname=fuente, fontsize=tamano, color=color)

                # Guarda el archivo PDF modificado en un archivo temporal
                temp_archivo = os.path.join(ruta_carpeta, 'temp.pdf')
                doc.save(temp_archivo)

                # Cierra el documento
                doc.close()

                # Reemplaza el archivo original con el archivo temporal
                shutil.move(temp_archivo, os.path.join(ruta_carpeta, archivo))
            except Exception as e:
                print(f"Error al procesar el archivo {archivo}: {e}")

# Usa la función en la ruta de la carpeta que desees
agregar_texto_a_pdf("C:\\AUTOM\\SPU")