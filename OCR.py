import PyPDF2
import pytesseract
from PIL import Image
import io

# Abre el archivo PDF
pdf_file = "4t8601ni.pdf"
pdf = PyPDF2.PdfFileReader(open(pdf_file, "rb"))

# Inicializa una variable para almacenar el texto extraído
texto_extraido = ""

# Itera a través de las páginas del PDF
for page_num in range(pdf.getNumPages()):
    # Extrae el texto de la página del PDF
    text = pdf.getPage(page_num).extractText()
    
    # Agrega el texto extraído a la variable
    texto_extraido += text

# Convierte el texto extraído en una imagen (esto es opcional)
image = Image.open(io.BytesIO(texto_extraido.encode('utf-8')))

# Realiza OCR en la imagen utilizando pytesseract
texto_ocr = pytesseract.image_to_string(image)

# Imprime el texto OCR
print(texto_ocr)