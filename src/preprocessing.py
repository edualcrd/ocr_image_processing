from pathlib import Path

import cv2


def load_image(image_path: str | Path):
    #Cargamos una imagen utilizando OpenCV.
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")
    return image


def preprocess_image(image):
    ## Aplica diferentes técnicas de preprocesamiento:
    #1. Escala de grises.
    #2. Reescalado si la imagen es pequeña.
    #3. Mejora del contraste.
    # 4. Eliminación de ruido.
    #5. Umbralización mediante Otsu.
    

    # 1. Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Aumentar resolución si la imagen es pequeña
    if max(gray.shape) < 1800:
        gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # 3. Mejorar el contraste
    clahe = cv2.createCLAHE( clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 4. Reducir ruido
    denoised = cv2.medianBlur(enhanced, 3)

    # 5. Aplicar umbralización Otsu
    _, processed = cv2.threshold(denoised, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return processed


def save_processed_image(image, original_path, output_dir):
    
    #Guarda la imagen procesada en formato PNG.
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(original_path).stem
    output_path = output_dir / f"{original_name}_procesada.png"

    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise RuntimeError(f"No se pudo guardar la imagen: {output_path}")
    return output_path
