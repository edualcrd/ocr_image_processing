import re


# Convierte los textos OCR de cada imagen en registros individuales, conservando el número de línea y la imagen de procedencia.
def structure_text_lines(results):

    records = []

    for result in results:

        # Ignorar las imágenes que hayan producido algúnos errores
        if result.get("error"):
            continue

        text = result.get("texto_limpio", "")

        # Separar el texto en líneas
        lines = text.splitlines()

        for line_number, line in enumerate(lines, start=1):

            # Normalizar espacios
            clean_line = " ".join(line.split())

            # Ignorar líneas vacías
            if not clean_line:
                continue

            records.append({"imagen": result["imagen"], "numero_linea": line_number, "confianza_media_imagen": result["confianza_media"], "texto_linea": clean_line})

    return records

#Extrae eventos de la cronología de ascenso del Apollo 11.
def extract_apollo_timeline_events(line_records):   

    # Identifica:
    # Tiempo transcurrido.
    # Código de responsable.
    # Descripción del evento.

    events = []

    target_image = "apollo 11 ascent timeline.webp"

    # Patrón (expresión regular) para detectar tiempos y códigos de eventos (Proporcionado por IA)
    pattern = re.compile(
        r"^\s*[\W_]*\s*"
        r"(?P<time>\d{1,2}:\d{2}(?:\.\d+)?)\s+"
        r"(?:(?P<code>[A-Z]{2,4})\s*:\s*)?"
        r"(?P<description>.*?)\s*$"
    )

    for record in line_records:

        # Trabajar únicamente con la cronología Apollo 11
        if record["imagen"] != target_image:
            continue

        original_line = record["texto_linea"]

        match = pattern.match(original_line)

        if not match:
            continue

        description = match.group("description").strip()

        if not description:
            continue

        events.append({
            "imagen": record["imagen"],
            "numero_linea": record["numero_linea"],
            "tiempo": match.group("time"),
            "codigo": match.group("code") or "",
            "descripcion": description,
            "confianza_media_imagen": (
                record["confianza_media_imagen"]
            ),
            "texto_original": original_line
        })

    return events
