import csv
from pathlib import Path

from src.ocr import clean_text, extract_text, get_ocr_confidence, save_text
from src.preprocessing import load_image, preprocess_image, save_processed_image
from src.structuring import extract_apollo_timeline_events, structure_text_lines

# Directorios del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

ORIGINAL_DIR = PROJECT_ROOT / "data" / "original"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Formatos de imagen compatibles
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff")

# Aquí procesamos una imagen completa: carga, preprocesa, reconoce y guarda el resultado.
def process_image(image_path):
    print(f"\nProcesando: {image_path.name}")

    # Cargar la imagen original
    original = load_image(image_path)

    # Preprocesamiento con OpenCV
    processed = preprocess_image(original)

    # Guardar imagen procesada
    processed_path = save_processed_image(processed, image_path, PROCESSED_DIR)

    # Extraemos texto por OCR
    raw_text = extract_text(processed, lang="eng")

    # Limpiar y normalizar el texto
    cleaned_text = clean_text(raw_text)
    # Calculamos la confianza del reconocimiento
    metrics = get_ocr_confidence(processed, lang="eng")

    # Guardamos el texto individual
    txt_path = OUTPUT_DIR / f"{image_path.stem}.txt"
    save_text(cleaned_text, txt_path)

    print(f"Palabras reconocidas: {metrics['recognized_words']}")
    print(f"Confianza media: {metrics['average_confidence']}%")

    return {"imagen": image_path.name, "imagen_procesada": processed_path.name,"palabras_reconocidas": metrics["recognized_words"], "confianza_media": metrics["average_confidence"], "texto_original": raw_text, "texto_limpio": cleaned_text, "error": ""}


def main():

    # Crear directorios de salida
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Obtener todas las imágenes originales
    image_paths = sorted(path for path in ORIGINAL_DIR.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS)

    if not image_paths:
        raise FileNotFoundError(f"No se encontraron imágenes en {ORIGINAL_DIR}")

    print(f"Se han encontrado {len(image_paths)} imágenes.")

    results = []

    # Procesar todas las imágenes
    for image_path in image_paths:

        try:
            result = process_image(image_path)
            results.append(result)

        except Exception as error:
            print(f"Error procesando {image_path.name}: {error}")

            results.append({"imagen": image_path.name, "imagen_procesada": "", "palabras_reconocidas": 0, "confianza_media": 0, "texto_original": "", "texto_limpio": "", "error": str(error)})

    # Exportar resultados generales a CSV
    csv_path = OUTPUT_DIR / "resultados.csv"

    fieldnames = ["imagen","imagen_procesada", "palabras_reconocidas", "confianza_media", "texto_original", "texto_limpio", "error"]

    with csv_path.open("w",newline="", encoding="utf-8-sig") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


    # Estructurar los textos OCR por líneas
    line_records = structure_text_lines(results)

    # Exportar segundo CSV
    line_csv_path = OUTPUT_DIR / "resultados_lineas.csv"

    line_fieldnames = ["imagen", "numero_linea", "confianza_media_imagen", "texto_linea"]

    with line_csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=line_fieldnames)

        writer.writeheader()
        writer.writerows(line_records)


    # Extraer eventos de la cronología Apollo 11
    apollo_events = extract_apollo_timeline_events(
        line_records
    )

    # Exportar eventos estructurados
    events_csv_path = OUTPUT_DIR / "apollo11_eventos.csv"

    event_fieldnames = ["imagen", "numero_linea", "tiempo", "codigo", "descripcion", "confianza_media_imagen", "texto_original"]

    with events_csv_path.open("w", newline="", encoding="utf-8-sig") as csv_file:

        event_writer = csv.DictWriter(csv_file, fieldnames=event_fieldnames)

        event_writer.writeheader()
        event_writer.writerows(apollo_events)

    print(f"Eventos Apollo 11 extraídos: {len(apollo_events)}")
    print(f"CSV de eventos: {events_csv_path}")


    # Resumen final
    successful = sum(1 for result in results if not result["error"])

    failed = len(results) - successful

    print("\n RESUMEN FINAL ")
    print(f"Total de imágenes: {len(image_paths)}")
    print(f"Procesadas correctamente: {successful}")
    print(f"Errores: {failed}")
    print(f"Archivo CSV: {csv_path}")
    print(f"Líneas de texto estructuradas: {len(line_records)}")
    print(f"CSV por líneas: {line_csv_path}")


if __name__ == "__main__":
    main()
