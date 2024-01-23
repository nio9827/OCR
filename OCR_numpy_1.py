import os
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import fitz  # PyMuPDF

# Ruta del directorio que contiene los archivos PDF
pdf_directory = "2827_C"

# Obtener la lista de archivos PDF en el directorio
pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith(".pdf")]

# Iterar sobre cada archivo PDF en el directorio
for pdf_file in pdf_files:
    # Construir la ruta completa del archivo PDF
    pdf_path = os.path.join(pdf_directory, pdf_file)

    # Abrir el archivo PDF con PyMuPDF (Fitz)
    pdf_document = fitz.open(pdf_path)

    # Obtener solo la primera página del PDF
    page = pdf_document[0]

    # Extraer las imágenes de la página
    images = page.get_images(full=True)

    # Iterar sobre cada imagen en la página
    for img_index, img_info in enumerate(images):
        # Obtener las coordenadas y tamaño de la imagen
        img_xref = img_info[0]
        img_base_image = pdf_document.extract_image(img_xref)
        img_bytes = img_base_image["image"]
        img_filename = f"{pdf_file}_page_1_img_{img_index + 1}.png"

        # Guardar la imagen en un archivo PNG
        with open(img_filename, "wb") as img_file:
            img_file.write(img_bytes)

        # Procesar la imagen como se hacía anteriormente
        imagen = Image.open(img_filename)
        array_imagen = np.array(imagen)
        # ... (resto del código para procesar la imagen)
        
        inicio_fila, fin_fila = 25, 90
        inicio_columna, fin_columna = 1135, 1435

        # Seleccionar la sección específica del array
        seccion_especifica = array_imagen[inicio_fila:fin_fila, inicio_columna:fin_columna]

        # Guardar la imagen de la sección específica
        Image.fromarray(seccion_especifica).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica.jpg")

        # Convertir la sección específica a escala de grises
        seccion_grises = Image.fromarray(seccion_especifica).convert('L')

        # Utilizar pytesseract para realizar OCR en la sección específica
        texto_detectado = pytesseract.image_to_string(seccion_grises, config='--psm 6', output_type=Output.STRING)

        # Imprimir el texto detectado
        print("Texto detectado en la sección específica:")
        print(texto_detectado)

    # Cerrar el documento PDF actual
    pdf_document.close()
