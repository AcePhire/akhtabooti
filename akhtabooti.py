import sys
import shutil
from pathlib import Path

import pytesseract
import cv2
from pdf2image import convert_from_path

from file_utils import * 

TERM_WIDTH, TERM_HEIGHT = shutil.get_terminal_size()

def help():
    print("Usage: python akhtabooti.py <directory to scan> \n")

def scan_image(image):
    return pytesseract.image_to_string(image)

if __name__ == "__main__":
    # Get directory
    if len(sys.argv) < 2:
        help()
        sys.exit(0)

    directory = Path(sys.argv[1])

    # Scan directory
    for entry in directory.iterdir():
        if entry.is_file():
            print(f"Scanning {entry.name}...")
            file = str(entry)

            # Handle file according to type
            if is_image(file):
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

