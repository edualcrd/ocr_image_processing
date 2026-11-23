import re
import shutil
import unicodedata
from pathlib import Path

import pytesseract
from PIL import Image
from pytesseract import Output

# Detectar automáticamente el ejecutable de Tesseract
tesseract_path = shutil.which("tesseract")

if tesseract_path is None:
    raise RuntimeError(
        "No se ha encontrado Tesseract OCR. "
        "Comprueba que está instalado y añadido al PATH del sistema."
    )

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Esta función reconoce el texto de una imagen ya procesada utilizando Tesseract.
def extract_text(image, lang="eng", psm=6): # Utilizo --psm 6 para que Tesseract trate la imagen como un solo bloque de texto.
    # Args:
        # image: Imagen procesada mediante OpenCV.
        # lang: Idioma del reconocimiento.
        # psm: Modo de segmentación de página de Tesseract.

    # Returns:
        # Texto reconocido.
    


    # Convertir el array de OpenCV a imagen PIL
    pil_image = Image.fromarray(image)

    # Configuración del motor OCR
    config = f"--oem 3 --psm {psm}"

    # Reconocimiento de texto
    text = pytesseract.image_to_string(pil_image, lang=lang, config=config)
    return text.strip()

    # Esta función calcula la confianza media de las palabras reconocidas.
def get_ocr_confidence(image, lang="eng", psm=6):
    
    # Returns:
        # Diccionario con confianza media y número de palabras.
    
    pil_image = Image.fromarray(image)
    config = f"--oem 3 --psm {psm}"

    data = pytesseract.image_to_data(pil_image, lang=lang,config=config, output_type=Output.DICT)

    confidences = []
    recognized_words = 0

    for word, confidence in zip(data["text"], data["conf"]):

        if word.strip() and float(confidence) >= 0:
            confidences.append(float(confidence))
            recognized_words += 1

    if confidences:
        average_confidence = round(sum(confidences) / len(confidences), 2)
    else:
        average_confidence = 0.0

    return {"average_confidence": average_confidence, "recognized_words": recognized_words}

# Esta guarda el texto reconocido en un archivo TXT.
def save_text(text, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(text, encoding="utf-8")

## La confianza que devuelve tesserac es una estimación del reconocimiento no una garantía de que el texto sea 100% correcto.abs


# Limpia y normaliza el texto obtenido mediante OCR.
def clean_text(text):
  
    # Normaliza caracteres Unicode.
    # Elimina caracteres de control innecesarios.
    # Sustituye espacios no separables.
    # Elimina espacios al final de cada línea.
    # Reduce saltos de línea excesivos.

    # Conserva los saltos de línea y la estructura interna del texto para no perder información.

    if not isinstance(text, str):
        raise TypeError("El texto debe ser una cadena.")

    # Normalizar caracteres Unicode
    text = unicodedata.normalize("NFC", text)

    # Normalizar saltos de línea
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Sustituir espacios no separables
    text = text.replace("\u00a0", " ")

    # Eliminar caracteres de control innecesarios
    text = text.replace("\x00", "")
    text = text.replace("\x0c", "")
    text = text.replace("\ufeff", "")

    # Eliminar espacios al final de cada línea
    lines = [line.rstrip() for line in text.split("\n")]

    text = "\n".join(lines)

    # Reducir tres o más saltos de línea a dos
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
