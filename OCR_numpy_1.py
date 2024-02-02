import os
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import fitz  # PyMuPDF

# Ruta del directorio que contiene los archivos PDF
pdf_directory = "rosada"
cont = 0


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
        

        inicio_fila, fin_fila = 25, 90
        inicio_columna, fin_columna = 1135, 1425

        # Seleccionar la sección específica del array
        seccion_especifica = array_imagen[inicio_fila:fin_fila, inicio_columna:fin_columna]
        
        
        #inicio_fila_v2, fin_fila_v2 = 90, 140
        #inicio_columna_v2, fin_columna_v2= 1200, 1430

        # Seleccionar la sección específica del array
        #seccion_especifica_v2 = array_imagen[inicio_fila_v2:fin_fila_v2, inicio_columna_v2:fin_columna_v2]
        
        #print ('parametros ' , array_imagen.shape)
        #----------------------------------------------------
        
        
        # Guardar la imagen de la sección específica
        Image.fromarray(seccion_especifica).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica.jpg")
        
        # Guardar la imagen de la sección específica
        #Image.fromarray(seccion_especifica_v2).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_v2.jpg")

        
        # Convertir la sección específica a escala de grises
        seccion_grises = Image.fromarray(seccion_especifica).convert('L')
        #seccion_grises_v2= Image.fromarray(seccion_especifica_v2).convert('L')
        
        #seccion_grises.save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_grises.jpg")
        #seccion_grises_v2.save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_grises_2.jpg")

        # Utilizar pytesseract para realizar OCR en la sección específica
        texto_detectado = pytesseract.image_to_string(seccion_grises, config='--psm 6', output_type=Output.STRING)
        #texto_detectado_v2 = pytesseract.image_to_string(seccion_grises_v2, config='--psm 6', output_type=Output.STRING)

        
        
        with open("probando.txt", "a") as archivo:
            archivo.write(texto_detectado)
        print(f"El número {texto_detectado} fue guardado en 'numero_encontrado.txt'")

        
        
        # resultados
        cont = cont +1
        
        # Imprimir el texto detectado
        print("Texto detectado en la sección específica:")
        print(texto_detectado)
        #print (texto_detectado_v2)
        print ('cantidad : ', cont)
    # Cerrar el documento PDF actual
    pdf_document.close()
