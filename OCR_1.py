import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import re
import os

# Ruta del archivo PDF
pdf_path = 'pdf_prueba/4t80lm3e.pdf'

# Función para extraer texto de un archivo PDF usando Tesseract OCR
def extract_text_from_pdf(pdf_path):
    # Abre el archivo PDF
    with open(pdf_path, 'rb') as file:
        # Lee el archivo PDF con PyPDF2
        try:
            pdf_reader = PdfReader(file)
        except Exception as e:
            print("Error al abrir el archivo PDF:", e)

        
        # Inicializa una variable para almacenar el texto extraído
        extracted_text = ''
        
        # Itera a través de cada página del PDF
        for page_num in range(len(pdf_reader.pages)):
            # Extrae el texto de cada página
            page = pdf_reader.pages[page_num]
            
            # Convierte la página del PDF a una imagen
            images = convert_from_path(pdf_path, dpi=300, first_page=page_num+1, last_page=page_num+1)
            
            # Utiliza OCR para extraer texto de la imagen
            text = pytesseract.image_to_string(images[0])
            
            # Agrega el texto extraído al texto acumulado
            extracted_text += text + '\n'
            print (extracted_text)
    
    return extracted_text

# Llama a la función para extraer texto del PDF
extracted_text = extract_text_from_pdf(pdf_path)

# Imprime el texto extraído
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
    if os.path.exists('4t8601ni.pdf'):
        os.rename('4t8601ni.pdf', nombre_rename)
        print(f"El archivo ha sido renombrado a '{nombre_rename}'")
    else:
        print("El archivo original no fue encontrado")
    
    
    with open('numero_encontrado.txt', 'w') as archivo:
        archivo.write(numero)
    print(f"El número {numero} fue guardado en 'numero_encontrado.txt'")
else:
    print("No se encontró ningún número en el texto")