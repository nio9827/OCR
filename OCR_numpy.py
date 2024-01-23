from PIL import Image
import numpy as np
import pytesseract
from pytesseract import Output

# Cargar la imagen desde un archivo
imagen_path = "4t80lm3c_page-0001.jpg"
imagen = Image.open(imagen_path)

# Convertir la imagen a un array NumPy
array_imagen = np.array(imagen)


# Definir las coordenadas de la sección específica
inicio_fila, fin_fila = 25, 80
inicio_columna, fin_columna = 850, 1080

# Seleccionar la sección específica del array
seccion_especifica = array_imagen[inicio_fila:fin_fila, inicio_columna:fin_columna, :]

# Guardar la imagen de la sección específica
Image.fromarray(seccion_especifica).save("C:/Users/aalveo/Pictures/probando/OCR/seccion_especifica.jpg")

# Convertir la sección específica a escala de grises
seccion_grises = Image.fromarray(seccion_especifica).convert('L')

# Utilizar pytesseract para realizar OCR en la sección específica
texto_detectado = pytesseract.image_to_string(seccion_grises, config='--psm 6', output_type=Output.STRING)

# Imprimir el texto detectado
print("Texto detectado en la sección específica:")
print(texto_detectado)



#print ('dimension de la imagen: ', array_imagen.shape)
