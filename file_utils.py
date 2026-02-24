from unstructured.partition.auto import partition
import easyocr

from PIL import Image

import io
from zipfile import ZipFile as zip_file
from pdf2image import convert_from_path

# Path where media is saved in documents
MEDIA_PATHS = {
    ".odt": "Pictures/",
    ".ods": "Pictures/",
    ".odp": "Pictures/",
    ".odg": "Pictures/",
    ".docx": "word/media/",
    ".xlsx": "xl/media/",
    ".pptx": "ppt/media/",
}

# Check if the file is an image file
def is_image(file):
    try:
        i = Image.open(file)
        return True
    except:
        return False

# Check if the file is a pdf file
def is_pdf(file):
    try:
        convert_from_path(file, 100)
        return True
    except:
        return False

# Load OCR reader into memory
def initialize_ocr(langs):
    return easyocr.Reader(langs, gpu=False)

# Extract text from image
def scan_image(image, ocr):
    results = ocr.readtext(image, detail=0)
    return "\n".join(artifact for artifact in results)

# Extract text from pdf
def scan_pdf(file, ocr):
    text = ""

    pdf_pages = convert_from_path(file, 400)
    for page in pdf_pages:
        text += scan_image(page, ocr)

    return text

# Extract text from the images within documents
def scan_document_images(file, ocr):
    text = ""

    images = []
    with zip_file(file, "r") as z:
        images = [f for f in z.namelist() if f.startswith("Pictures/")]

        for image_path in images:
                with z.open(image_path) as f:
                    image = Image.open(io.BytesIO(f.read()))
                    text += scan_image(image, ocr)

    return text

# Extract text from documents
def extract_text(file, ocr):
    elements = partition(filename=file, strategy="auto", include_page_breaks=True)

    text = "".join(str(element) for element in elements)
    try:
        text += scan_document_images(file, ocr)
    except:
        pass

    return text
