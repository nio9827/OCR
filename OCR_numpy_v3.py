import os
import re 
import numpy as np
from PIL import Image
import shutil
import fitz  # PyMuPDF
import easyocr

# Ruta del directorio que contiene los archivos PDF
pdf_directory = "C:/Users/aalveo/Desktop/CEPADEM/DATA/01/80/2805_C"
cont = 0
factor_zoom = 2
nombre_CSV = 'C:/Users/aalveo/Pictures/probando/OCR/banco_csv/80/2805_C'
seccion_img = 'C:/Users/aalveo/Desktop/CEPADEM/DATA/01/80/2805_C/2805_img'
nueva_ruta_directorio = 'C:/Users/aalveo/Desktop/CEPADEM/DATA/01/80/2805_C/archivos_re'

# Crear un objeto EasyOCR con el idioma deseado
reader = easyocr.Reader(['en'])

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
        ruta_completa = os.path.join("img", img_filename)

        # Guardar la imagen en un archivo PNG en la carpeta de destino
        with open(ruta_completa, "wb") as img_file:
            img_file.write(img_bytes)

        # Procesar la imagen después de guardarla
        imagen = Image.open(ruta_completa)
        array_imagen = np.array(imagen)
        
        inicio_fila, fin_fila = 25, 100
        inicio_columna, fin_columna = 1135, 1430

        # Seleccionar la sección específica del array
        seccion_especifica = array_imagen[inicio_fila:fin_fila, inicio_columna:fin_columna]
        
        # Convertir la sección específica a escala de grises
        seccion_grises = Image.fromarray(seccion_especifica).convert('L')
        
        # Realiza un zoom en la imagen
        nuevo_ancho = seccion_grises.width * factor_zoom
        nueva_altura = seccion_grises.height * factor_zoom
        imagen_zoom = seccion_grises.resize((nuevo_ancho, nueva_altura))
        
        # Utilizar EasyOCR para realizar OCR en la sección específica
        resultados = reader.readtext(np.array(imagen_zoom))

        # Procesar los resultados de EasyOCR
        for resultado in resultados:
            texto_detectado = resultado[1]
            digitos_extraidos = re.search(r"\b\d{9}\b", texto_detectado)
            
            if digitos_extraidos:
                text = digitos_extraidos.group(0) 
                nombre_rename = text + ".pdf"
                
                # Guardar la sección de imagen con el texto extraído
                imagen_zoom.save(os.path.join(seccion_img, text + '.jpg'))
                
                # Renombrar el archivo PDF original
                nueva_ruta_pdf = os.path.join(nueva_ruta_directorio, nombre_rename)

                try:
                    with open(pdf_path, 'rb') as archivo_original:
                        with open(nueva_ruta_pdf, 'wb') as archivo_renombrado:
                            shutil.copyfileobj(archivo_original, archivo_renombrado)
                    print(f"El archivo '{pdf_file}' ha sido renombrado como '{nombre_rename}' en la nueva ruta '{nueva_ruta_pdf}'.")
                    # Eliminar el archivo original
                    os.remove(pdf_path)
                except PermissionError:
                    print(f"")
                
                # Crear el archivo CSV
                with open(nombre_CSV + ".csv", "a") as archivo:
                    archivo.write(text + ';' + pdf_file + '; \n')
                print(f"El número {text} fue guardado en {nombre_CSV} \n")
                print(f"Texto detectado en la sección específica: {text}")
                print('Nombre del archivo: ' + pdf_file)
                cont += 1
                print (f"Total: {cont}")
                
            else: 
                print ("//////////////////////////////////////\n")
                print (f'Archivos no detectado {pdf_file}')
                
                try:
                    ruta_origen = os.path.join(pdf_directory, pdf_file)
                    ruta_destino = os.path.join(pdf_directory, 'inc', pdf_file)
                    shutil.move(ruta_origen, ruta_destino)
                except:
                    print (f'Error al detectar N° Cepadem: archivo  {pdf_file}')
                print ("////////////////////////////////////// \n")
    # Cerrar el documento PDF actual
    pdf_document.close()
