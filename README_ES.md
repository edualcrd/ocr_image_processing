# OCR de imágenes con OpenCV y PyTesseract

Proyecto de la asignatura **Sistemas de Big Data** para extraer texto de imágenes, aplicar técnicas de preprocesamiento y convertir los resultados del OCR en archivos estructurados.

El proyecto utiliza **OpenCV** para preparar las imágenes y **Tesseract OCR**, mediante **PyTesseract**, para reconocer el texto. Los resultados se guardan en archivos TXT y CSV para facilitar su consulta y análisis posterior.

## Objetivos

- Leer imágenes de distintos formatos con OpenCV.
- Aplicar técnicas de preprocesamiento para facilitar el reconocimiento de caracteres.
- Extraer texto de las imágenes mediante Tesseract OCR.
- Limpiar y normalizar el texto reconocido sin alterar deliberadamente su contenido.
- Transformar los textos en registros por línea y en campos concretos cuando se reconoce un patrón conocido.
- Exportar los resultados a formatos TXT y CSV.
- Identificar las limitaciones y los errores que pueden aparecer al aplicar OCR a imágenes de diferente calidad.

## Tecnologías utilizadas

- **Python 3.12**
- **OpenCV (`opencv-python`)**: carga y preprocesamiento de imágenes.
- **Tesseract OCR 5**: motor externo de reconocimiento óptico de caracteres.
- **PyTesseract**: integración de Tesseract con Python.
- **Pillow**: conversión de imágenes entre formatos compatibles con las librerías utilizadas.
- **Matplotlib**: visualización de imágenes durante las pruebas de preprocesamiento.
- **Pandas**: disponible en el entorno para análisis de datos tabulares.
- **CSV**: exportación de los resultados mediante el módulo estándar de Python.

## Estructura del proyecto

```text
OCR/
├── data/
│   ├── original/             # Imágenes originales de entrada
│   └── processed/            # Imágenes después del preprocesamiento
│
├── output/
│   ├── *.txt                 # Texto OCR de cada imagen
│   ├── resultados.csv        # Resumen y texto por imagen
│   ├── resultados_lineas.csv # Texto dividido en líneas
│   └── apollo11_eventos.csv  # Eventos extraídos de la cronología Apollo 11
│
├── notebooks/                # Cuadernos de experimentación (si se utilizan)
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py      # Carga y preprocesamiento con OpenCV
│   ├── ocr.py                # Reconocimiento, confianza y limpieza de texto
│   ├── structuring.py        # Estructuración por líneas y eventos Apollo 11
│   └── main.py               # Flujo principal del proyecto
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalación y configuración

### 1. Clonar el repositorio

El proyecto se encuentra dentro del repositorio del curso, en `Sistemas_de_Big_Data/OCR`.

```powershell
git clone https://github.com/edualcrd/AI_Big_Data_Course.git
cd AI_Big_Data_Course
```

Si ya tienes el repositorio clonado, entra directamente en su carpeta local.

### 2. Crear o activar el entorno virtual

En el entorno de desarrollo utilizado para el curso se comparte un único entorno `uv` desde la raíz del repositorio, para que las distintas asignaturas puedan utilizar las mismas dependencias.

Si todavía no existe un entorno virtual en esa ubicación, créalo una sola vez:

```powershell
uv venv .venv
```

Actívalo desde la raíz del repositorio:

```powershell
.\.venv\Scripts\Activate.ps1
```

No es necesario crear otro entorno dentro de `OCR` si se utiliza el entorno compartido.

### 3. Instalar las dependencias de Python

Desde la carpeta del proyecto OCR:

```powershell
cd .\Sistemas_de_Big_Data\OCR
uv pip install -r requirements.txt
```

También se puede utilizar `pip` desde el entorno virtual activado:

```powershell
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene las dependencias Python del proyecto:

```text
opencv-python
pytesseract
pillow
matplotlib
pandas
```

### 4. Instalar Tesseract OCR

**PyTesseract no instala el motor Tesseract**. Es necesario instalarlo por separado en el sistema operativo.

En Windows se puede utilizar el instalador de UB Mannheim:

<https://github.com/UB-Mannheim/tesseract/wiki>

Durante la instalación, asegúrate de disponer del idioma inglés (`eng`), utilizado en el reconocimiento de este proyecto.

Comprueba la instalación desde PowerShell:

```powershell
tesseract --version
tesseract --list-langs
```

En `src/ocr.py` se configura la ruta del ejecutable de Tesseract. En el entorno de desarrollo utilizado es:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

Si Tesseract está instalado en otra ubicación, modifica esa ruta para que apunte al archivo `tesseract.exe` correspondiente. También se puede añadir la carpeta de instalación a la variable de entorno `PATH` de Windows.

## Ejecución

Coloca las imágenes que quieras procesar en:

```text
data/original/
```

Desde la carpeta `OCR`, con el entorno virtual activado, ejecuta:

```powershell
python -m src.main
```

El programa busca imágenes con extensiones compatibles (PNG, JPG, JPEG, WEBP, BMP, TIF y TIFF), procesa cada archivo y guarda los resultados en `data/processed/` y `output/`.

## Funcionamiento del proceso

### 1. Carga y preprocesamiento de imágenes

El módulo `preprocessing.py` carga las imágenes con OpenCV y aplica una secuencia de transformaciones:

1. Conversión a escala de grises.
2. Reescalado de las imágenes pequeñas para facilitar la lectura.
3. Mejora del contraste local mediante CLAHE.
4. Reducción de ruido con un filtro de mediana.
5. Umbralización binaria mediante el método de Otsu.

Las imágenes procesadas se guardan en `data/processed/` para poder inspeccionar visualmente el resultado.

### 2. Reconocimiento OCR

El módulo `ocr.py` convierte la matriz de OpenCV en una imagen compatible con Pillow y utiliza PyTesseract para extraer el texto. La configuración empleada utiliza el idioma inglés (`eng`) y el modo de segmentación de página `--psm 6`.

Además del texto, se obtiene una estimación de confianza de Tesseract a partir de los datos reconocidos por palabra. Esta confianza es una señal orientativa del motor, **no una medida de exactitud verificada**.

### 3. Limpieza y normalización

La función `clean_text()` normaliza caracteres Unicode, espacios no separables, caracteres de control y saltos de línea repetidos. La limpieza es conservadora: no intenta adivinar ni sustituir palabras que el OCR haya podido reconocer incorrectamente.

### 4. Estructuración por líneas

El módulo `structuring.py` divide el texto limpio en líneas no vacías. Cada registro conserva el nombre de la imagen de origen, el número de línea, la confianza media de la imagen y el contenido de esa línea.

### 5. Extracción de eventos de Apollo 11

El proyecto incluye una extracción específica para la imagen `apollo 11 ascent timeline.webp`. Mediante una expresión regular se buscan líneas que contengan un tiempo y, cuando aparece, un código de evento y una descripción. Esta extracción depende del formato del documento y del texto que haya reconocido Tesseract; no se aplica de forma general a todas las imágenes.

## Archivos de salida

| Archivo | Contenido |
|---|---|
| `output/<nombre_imagen>.txt` | Texto limpio reconocido para cada imagen. |
| `output/resultados.csv` | Una fila por imagen, con nombre, imagen procesada, número de palabras, confianza media, texto original, texto limpio y posible error. |
| `output/resultados_lineas.csv` | Una fila por línea no vacía, con imagen de origen, número de línea, confianza media de la imagen y texto de la línea. |
| `output/apollo11_eventos.csv` | Eventos de la cronología Apollo 11 que coinciden con el patrón de extracción, separados en tiempo, código y descripción, entre otros campos de trazabilidad. |

## Resultados y limitaciones

El conjunto de entrada utilizado contiene **23 imágenes**. En el archivo `resultados_lineas.csv` generado durante la ejecución revisada se observan **726 líneas no vacías** distribuidas entre esas 23 imágenes.

La calidad del reconocimiento varía según la resolución, el contraste, la orientación, la tipografía y la complejidad de cada imagen. En los resultados revisados, la confianza media por imagen proporcionada por Tesseract se situó aproximadamente entre **26,67 y 83,44**. Varias imágenes presentaron valores inferiores a 40, por lo que sus textos requieren una revisión manual especialmente cuidadosa.

Estas cifras describen la salida del motor OCR y **no significan que ese porcentaje de caracteres o palabras sea necesariamente correcto**. Una confianza elevada tampoco garantiza que no existan errores. Por este motivo, los CSV deben revisarse antes de utilizar los datos en análisis que requieran exactitud.

La extracción de eventos de Apollo 11 es una regla específica para una imagen concreta. Las demás imágenes se procesan y se exportan como texto y líneas, pero no se convierten automáticamente en tablas semánticas de campos específicos.

## Posibles mejoras

- Comparar diferentes configuraciones de Tesseract (`--psm`) según el tipo de documento.
- Aplicar preprocesamientos alternativos para fotografías con baja confianza OCR.
- Detectar y corregir la orientación de las imágenes antes del reconocimiento.
- Extraer estructuras específicas para otros tipos de documentos, como tablas deportivas.
- Incorporar validaciones manuales y métricas de exactitud mediante una transcripción de referencia.
- Utilizar Pandas para análisis exploratorio de los CSV y detección de resultados anómalos.

## Repositorio

El proyecto forma parte del repositorio del curso:

<https://github.com/edualcrd/AI_Big_Data_Course>

Ruta del proyecto: `Sistemas_de_Big_Data/OCR/`.
