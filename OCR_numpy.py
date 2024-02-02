from PIL import Image
import numpy as np
import pytesseract
from pytesseract import Output

# Cargar la imagen desde un archivo
imagen_path = "imagen_zoom_negativa.jpg"
imagen = Image.open(imagen_path)

# Convertir la imagen a un array NumPy
array_imagen = np.array(imagen)


# Definir las coordenadas de la sección específica
inicio_fila_v2, fin_fila_v2 = 0, 150
inicio_columna_v2, fin_columna_v2= 0, 690

# Seleccionar la sección específica del array
seccion_especifica_v2 = array_imagen[inicio_fila_v2:fin_fila_v2, inicio_columna_v2:fin_columna_v2]

# Guardar la imagen de la sección específica
Image.fromarray(seccion_especifica_v2).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica_zoom.jpg")

# Convertir la sección específica a escala de grises
seccion_grises = Image.fromarray(seccion_especifica_v2).convert('L')

# Utilizar pytesseract para realizar OCR en la sección específica
texto_detectado = pytesseract.image_to_string(seccion_grises, config='--psm 6', output_type=Output.STRING)

# Imprimir el texto detectado
print("Texto detectado en la sección específica:")
print(texto_detectado)



print ('dimension de la imagen: ', array_imagen.shape)
