# Image OCR with OpenCV and PyTesseract

Project for the **Big Data Systems** course. Its purpose is to extract text from images, apply image preprocessing techniques, and convert OCR results into structured files.

The project uses **OpenCV** to prepare images and **Tesseract OCR**, through **PyTesseract**, to recognise text. Results are saved in TXT and CSV files to make them easier to inspect and analyse later.

## Objectives

- Read images in different formats with OpenCV.
- Apply preprocessing techniques to make character recognition easier.
- Extract text from images using Tesseract OCR.
- Clean and normalise the recognised text without deliberately changing its content.
- Convert the text into line-level records and into specific fields when a known pattern can be identified.
- Export the results to TXT and CSV formats.
- Identify the limitations and errors that can arise when applying OCR to images of varying quality.

## Technologies

- **Python 3.12**
- **OpenCV (`opencv-python`)**: image loading and preprocessing.
- **Tesseract OCR 5**: external optical character recognition engine.
- **PyTesseract**: Python integration for Tesseract.
- **Pillow**: image conversion between formats supported by the libraries used.
- **Matplotlib**: image visualisation during preprocessing tests.
- **Pandas**: available in the environment for tabular data analysis.
- **CSV**: results are exported using Python's built-in `csv` module.

## Project structure

```text
OCR/
├── data/
│   ├── original/             # Original input images
│   └── processed/            # Images after preprocessing
│
├── output/
│   ├── *.txt                 # OCR text for each image
│   ├── resultados.csv        # Summary and text for each image
│   ├── resultados_lineas.csv # Text split into individual lines
│   └── apollo11_eventos.csv  # Events extracted from the Apollo 11 timeline
│
├── notebooks/                # Experimentation notebooks (if used)
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py      # Image loading and preprocessing with OpenCV
│   ├── ocr.py                # Text recognition, confidence and cleaning
│   ├── structuring.py        # Line-level structuring and Apollo 11 events
│   └── main.py               # Main project workflow
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and configuration

### 1. Clone the repository

The project is located in the course repository, under `Sistemas_de_Big_Data/OCR`.

```powershell
git clone https://github.com/edualcrd/AI_Big_Data_Course.git
cd AI_Big_Data_Course
```

If you have already cloned the repository, go directly to its local directory.

### 2. Create or activate the virtual environment

The course development setup uses a single shared `uv` environment at the repository root so that different subjects can use the same dependencies.

If there is no virtual environment at that location yet, create it once:

```powershell
uv venv .venv
```

Activate it from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
```

There is no need to create another environment inside `OCR` when using the shared environment.

### 3. Install the Python dependencies

From the OCR project directory:

```powershell
cd .\Sistemas_de_Big_Data\OCR
uv pip install -r requirements.txt
```

You can also use `pip` from the activated virtual environment:

```powershell
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains the project's Python dependencies:

```text
opencv-python
pytesseract
pillow
matplotlib
pandas
```

### 4. Install Tesseract OCR

**PyTesseract does not install the Tesseract engine.** Tesseract must be installed separately on the operating system.

On Windows, you can use the UB Mannheim installer:

<https://github.com/UB-Mannheim/tesseract/wiki>

During installation, make sure the English language data (`eng`) is available, as it is used for text recognition in this project.

Check the installation from PowerShell:

```powershell
tesseract --version
tesseract --list-langs
```

In `src/ocr.py`, the path to the Tesseract executable is configured. The development environment uses:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

If Tesseract is installed in a different location, update this path so that it points to the relevant `tesseract.exe` file. You can also add the installation directory to the Windows `PATH` environment variable.

## Running the project

Place the images you want to process in:

```text
data/original/
```

From the `OCR` directory, with the virtual environment activated, run:

```powershell
python -m src.main
```

The program looks for images with supported extensions (PNG, JPG, JPEG, WEBP, BMP, TIF and TIFF), processes each file, and saves the results in `data/processed/` and `output/`.

## How the process works

### 1. Image loading and preprocessing

The `preprocessing.py` module loads images with OpenCV and applies a sequence of transformations:

1. Conversion to grayscale.
2. Upscaling of smaller images to make text easier to read.
3. Local contrast enhancement using CLAHE.
4. Noise reduction using a median filter.
5. Binary thresholding using Otsu's method.

The processed images are saved in `data/processed/` so that the results can be visually inspected.

### 2. OCR recognition

The `ocr.py` module converts the OpenCV array into an image compatible with Pillow and uses PyTesseract to extract the text. The configuration uses English (`eng`) and page segmentation mode `--psm 6`.

In addition to the text, the program obtains a confidence estimate from Tesseract's word-level recognition data. This confidence is an indicative signal from the engine, **not a verified accuracy measurement**.

### 3. Text cleaning and normalisation

The `clean_text()` function normalises Unicode characters, non-breaking spaces, control characters and repeated line breaks. The cleaning process is conservative: it does not attempt to guess or replace words that may have been recognised incorrectly by OCR.

### 4. Line-level structuring

The `structuring.py` module splits the cleaned text into non-empty lines. Each record retains the source image name, line number, the image's average confidence and the content of that line.

### 5. Apollo 11 event extraction

The project includes a specific extraction step for the `apollo 11 ascent timeline.webp` image. A regular expression is used to find lines containing a time and, when present, an event code and description. This extraction depends on the document's format and on the text recognised by Tesseract; it is not applied generically to all images.

## Output files

| File | Contents |
|---|---|
| `output/<image_name>.txt` | Cleaned OCR text recognised for each image. |
| `output/resultados.csv` | One row per image, including its name, processed image, word count, average confidence, original text, cleaned text and any error. |
| `output/resultados_lineas.csv` | One row per non-empty line, including source image, line number, image-level average confidence and line text. |
| `output/apollo11_eventos.csv` | Apollo 11 timeline events matching the extraction pattern, separated into time, code and description, along with traceability fields. |

## Results and limitations

The input dataset contains **23 images**. The `resultados_lineas.csv` file generated during the reviewed run contains **726 non-empty lines** across those 23 images.

Recognition quality varies depending on resolution, contrast, orientation, typography and image complexity. In the reviewed results, the average confidence per image reported by Tesseract ranged approximately from **26.67 to 83.44**. Several images had values below 40, so their recognised text requires particularly careful manual review.

These figures describe the OCR engine's output and **do not mean that the same percentage of characters or words is necessarily correct**. A high confidence score does not guarantee that there are no errors either. For this reason, the CSV files should be reviewed before the data is used in analyses that require accuracy.

Apollo 11 event extraction is a rule designed for one specific image. The other images are processed and exported as text and lines, but they are not automatically converted into semantic tables with document-specific fields.

## Possible improvements

- Compare different Tesseract configurations (`--psm`) depending on the document type.
- Apply alternative preprocessing techniques to photographs with low OCR confidence.
- Detect and correct image orientation before recognition.
- Extract specific structures from other document types, such as sports tables.
- Add manual validation and accuracy metrics using a reference transcription.
- Use Pandas for exploratory analysis of the CSV files and detection of unusual results.

## Repository

The project is part of the course repository:

<https://github.com/edualcrd/AI_Big_Data_Course>

Project path: `Sistemas_de_Big_Data/OCR/`.
