import sys
import shutil
from pathlib import Path

import pytesseract
import cv2
from pdf2image import convert_from_path

from text_utils import * 
from file_utils import * 

TERM_WIDTH, TERM_HEIGHT = shutil.get_terminal_size()

def help():
    print("Usage: python akhtabooti.py <directory to scan> \n")

def scan_image(image):
    return pytesseract.image_to_string(image)

def search_for_piis(text):
    rules = get_regexes()

    pii = {
        "email accounts": email_pii(rules, text),
        "phone numbers": phone_pii(rules, text),
        "keywords": keyword_pii(rules, text)
    }

    print(pii)

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

            search_for_piis(text) 
            print("-"*TERM_WIDTH)

