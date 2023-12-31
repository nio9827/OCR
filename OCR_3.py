
# binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#  técnicas de umbral adaptativo que se ajustan automáticamente en función de las características locales de la imagen.
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import cv2
import numpy as np
import re
import os


# Ruta del archivo PDF
carpeta_pdf = '2827_C'
cont = 0
# Función para aplicar un umbral a una imagen en escala de grises
def apply_threshold(image):
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary_image

# Función para extraer texto de un archivo PDF usando Tesseract OCR
def extract_text_from_pdf(pdf_path):
    # Abre el archivo PDF
    with open(pdf_path, 'rb') as file:
        # Lee el archivo PDF con PyPDF2
        try:
            pdf_reader = PdfReader(file)
        except Exception as e:
            print("Error al abrir el archivo PDF:", e)
            return None

        # Inicializa una variable para almacenar el texto extraído
        extracted_text = ''

        # Itera a través de cada página del PDF
        for page_num in range(len(pdf_reader.pages)):
            # Convierte la página del PDF a una imagen en escala de grises
            images = convert_from_path(pdf_path, dpi=300, first_page=page_num + 1, last_page=page_num + 1)
            gray_image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2GRAY)

            # Aplica un umbral a la imagen en escala de grises
            binary_image = apply_threshold(gray_image)

            # Utiliza OCR para extraer texto de la imagen binaria con PSM 7
            text = pytesseract.image_to_string(binary_image, config='--psm 6')

            # Agrega el texto extraído al texto acumulado
            extracted_text += text + '\n'

        return extracted_text
'''
# Llama a la función para extraer texto del PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Imprime el texto extraído


if extracted_text:
    print('Texto extraído:\n', extracted_text)
else:
    print('No se pudo extraer texto del PDF.')
    
'''

# Iterar sobre los archivos en la carpeta
for filename in os.listdir(carpeta_pdf):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(carpeta_pdf, filename)
        
        # Llama a la función para extraer texto del PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Imprimir el texto extraído
        print(extracted_text.split('\n')[1])

        # Patrón de expresión regular para encontrar números
        patron = r'\b\d{9}\b'

        # Buscar coincidencias con el patrón en el texto
        coincidencias = re.search(patron, extracted_text)

        # Imprimir el número extraído
        if coincidencias:
            numero = coincidencias.group(0)

            nombre_rename = numero + '.pdf'

            # Verificar si el archivo original existe y renombrarlo
            if os.path.exists(pdf_path):
                nuevo_path = os.path.join(carpeta_pdf, nombre_rename)
                os.rename(pdf_path, nuevo_path)
                print(f"El archivo '{filename}' ha sido renombrado a '{nombre_rename}'")
                
                cont = cont +1
                
                print ('Total',cont)
            else:
                print(f"El archivo '{filename}' no fue encontrado")

            with open('numero_encontrado.txt', 'a') as archivo:
                archivo.write(numero+';\n')
            print(f"El número {numero} fue guardado en 'numero_encontrado.txt'")
        else:
            print("No se encontró ningún número en el texto")
