import sys
import io
from pathlib import Path
from unstructured.partition.auto import partition
from unstructured.partition.image import partition_image
import pytesseract
from PIL import Image
import cv2
from pdf2image import convert_from_path
import shutil

TERM_WIDTH, TERM_HEIGHT = shutil.get_terminal_size()

def is_image(file_path):
    try:
        i=Image.open(file_path)
        return True
    except:
        return False

def is_pdf(file_path):
    try:
        convert_from_path(file_path, 100)
        return True
    except:
        return False

def scan_image(image):
    #buf = io.BytesIO()
    #image.save(buf, "PNG")
    #buf.seek(0)
    #elements = partition_image(file=buf)

    return pytesseract.image_to_string(image)


def extract_text(file_path):
    elements = partition(filename=file_path, strategy="auto", include_page_breaks=True)

    return "\n\n".join([str(element) for element in elements])


if __name__ == "__main__":
    directory = Path(sys.argv[1])

    for entry in directory.iterdir():
        if entry.is_file():
            print(f"Scanning {entry.name}...")

            file = str(entry)

            if is_image(file):
                #image = Image.open(file)
                image = cv2.imread(file)
                text = scan_image(image)
            elif is_pdf(file):
                pdf_pages = convert_from_path(file, 400)
                for page in pdf_pages:
                    text = scan_image(page)
            else:
                text = extract_text(file)

            print(text)
            print("-"*TERM_WIDTH)

