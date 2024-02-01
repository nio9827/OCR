import os
import re 
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import fitz  # PyMuPDF
import shutil

# Ruta del directorio que contiene los archivos PDF
pdf_directory = "m_p"
cont = 0
factor_zoom = 2
nombre_CSV = 'nombre_lote_01'

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
        inicio_columna, fin_columna = 1135, 1420

        # Seleccionar la sección específica del array
        seccion_especifica = array_imagen[inicio_fila:fin_fila, inicio_columna:fin_columna]
        
        #print ('parametros ' , array_imagen.shape)
        #----------------------------------------------------
        
        # Guardar la imagen de la sección específica
        #Image.fromarray(seccion_especifica).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica.jpg")
        
        # Guardar la imagen de la sección específica
        
        # Convertir la sección específica a escala de grises
        seccion_grises = Image.fromarray(seccion_especifica).convert('L')
        
        
        #Realiza un zoom en la imagen
        nuevo_ancho = seccion_grises.width * factor_zoom
        nueva_altura = seccion_grises.height * factor_zoom
        imagen_zoom = seccion_grises.resize((nuevo_ancho, nueva_altura))
        
        #Guarda la imagen
        #imagen_zoom.save('imagen_zoom_negativa.jpg')

        
        #seccion_grises.save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_grises.jpg")
        #seccion_grises_v2.save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_grises_2.jpg")

        # Utilizar pytesseract para realizar OCR en la sección específica
        texto_detectado = pytesseract.image_to_string(imagen_zoom, config='--psm 6', output_type=Output.STRING)
        
        
        patron = r"\b\d{9}\b"
        digitos_extraidos = re.search(patron, texto_detectado)
        
        if digitos_extraidos:
        
            text = digitos_extraidos.group(0) 
            nombre_rename = text + ".pdf"
            
            imagen_zoom.save('cepadem_img/'+text+'.jpg')
            '''
            if os.path.exists(pdf_path):
                nuevo_path = os.path.join(pdf_directory,nombre_rename)
                os.rename(pdf_path, nuevo_path)
                print(f"El archivo '{pdf_file}' ha sido renombrado a '{nombre_rename}'")
            else:
                print(f"No se pudo renombrar el archivo {pdf_file}")
            '''                
                
            with open(nombre_CSV+".csv", "a") as archivo:
                archivo.write(text+';'+ pdf_file+'; \n')
                
                
                
            print(f"El número {text} fue guardado en {nombre_CSV} \n")
            print("Texto detectado en la sección específica:")
            print(text)
            print('nombre del archivo: '+pdf_file)
            
            
            
        else: 
            print ("//////////////////////////////////////\n")
            print (f'Archivos no detectado {pdf_file}')
            
            try:
                ruta_origen = 'm_p/'+pdf_file
                ruta_destino = 'm_p/inc/'+pdf_file
                shutil.move(ruta_origen, ruta_destino)
            except:
                print (f'Error al detectar N° Cepadem: archivo  {pdf_file}')
            print ("////////////////////////////////////// \n")
            
            
        # resultados
        cont = cont +1
        
        # Imprimir el texto detectado
        #print ('cantidad : ', cont)
    # Cerrar el documento PDF actual
pdf_document.close()
