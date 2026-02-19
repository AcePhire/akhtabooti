from unstructured.partition.auto import partition
import easyocr

from PIL import Image

import cv2
from pdf2image import convert_from_path

# Check if the file is an image file
def is_image(file_path):
    try:
        i = Image.open(file_path)
        return True
    except:
        return False

# Check if the file is a pdf file
def is_pdf(file_path):
    try:
        convert_from_path(file_path, 100)
        return True
    except:
        return False

# Load OCR reader into memory
def initialize_ocr(langs):
    return easyocr.Reader(langs, gpu=False)

# Extract text from image
def scan_image(file, ocr):
    results = ocr.readtext(file, detail=0)
    return "\n".join(artifact for artifact in results)

# Extract text from pdf
def scan_pdf(file, ocr):
    text = ""

    pdf_pages = convert_from_path(file, 400)
    for page in pdf_pages:
        text += scan_image(page, ocr)

    return text

# Extract text from documents
def extract_text(file_path):
    elements = partition(filename=file_path, strategy="auto", include_page_breaks=True)

    return "\n".join([str(element) for element in elements])
