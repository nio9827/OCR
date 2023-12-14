# Función para extraer texto de un archivo PDF usando Tesseract OCR y guardarlo en un archivo de texto
def extract_text_and_save(pdf_path, output_txt):
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
            # Extrae el texto de cada página
            page = pdf_reader.pages[page_num]

            # Convierte la página del PDF a una imagen
            images = convert_from_path(pdf_path, dpi=300, first_page=page_num+1, last_page=page_num+1)

            # Utiliza OCR para extraer texto de la imagen
            text = pytesseract.image_to_string(images[0])

            # Agrega el texto extraído al texto acumulado
            extracted_text += text + ';\n'  # Punto y coma al final de cada extracto

    # Guarda el texto extraído en el archivo de texto especificado
    with open(output_txt, 'w') as output_file:
        output_file.write(extracted_text)

    return extracted_text


# Iterar sobre los archivos en la carpeta
for filename in os.listdir(carpeta_pdf):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(carpeta_pdf, filename)
        
        # Llama a la función para extraer texto del PDF y guardar en un archivo de texto
        output_txt = os.path.splitext(pdf_path)[0] + "_texto_extraido.txt"
        extracted_text = extract_text_and_save(pdf_path, output_txt)

        if extracted_text:
            print(f"Texto extraído del archivo '{filename}' y guardado en '{output_txt}'")
        else:
            print(f"No se pudo extraer texto del archivo '{filename}'")
