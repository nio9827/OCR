from PIL import Image

# Abre una imagen
imagen = Image.open('seccion_especifica.jpg')

# Define el factor de zoom (por ejemplo, 2 para duplicar el tamaño)
factor_zoom = 2

# Calcula el nuevo tamaño de la imagen
nuevo_ancho = imagen.width * factor_zoom
nueva_altura = imagen.height * factor_zoom

# Redimensiona la imagen al nuevo tamaño
imagen_zoom = imagen.resize((nuevo_ancho, nueva_altura))

# Convierte la imagen a modo "L" (escala de grises) si no está en ese modo
imagen_zoom_gris = imagen_zoom.convert('L')

# Invierte el contraste de la imagen (negativo)
#imagen_zoom_negativa = Image.eval(imagen_zoom_gris, lambda x: 255 - x)

# Guarda la imagen con contraste negativo
imagen_zoom_gris.save('imagen_zoom_negativa.jpg')

