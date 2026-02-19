import sys, shutil, json
from pathlib import Path

from text_utils import * 
from file_utils import * 

TERM_WIDTH, TERM_HEIGHT = shutil.get_terminal_size()

def help():
    print("Usage: python akhtabooti.py <directory to scan> \n")

def search_for_pii(text):
    rules = get_regexes()

    pii = {
        "email accounts": email_pii(rules, text),
        "phone numbers": phone_pii(rules, text),
        "other PIIs": keyword_pii(rules, text)
    }

    return pii

if __name__ == "__main__":
    # Get directory
    if len(sys.argv) < 2:
        help()
        sys.exit(0)

    directory = Path(sys.argv[1])

    ocr = initialize_ocr(["en"])

    results = {}

    # Scan directory
    for entry in directory.iterdir():
        if entry.is_file():
            print(f"Scanning {entry.name}...")
            file = str(entry)

            # Extract text from file according to its type
            if is_image(file):
                text = scan_image(file, ocr)
            elif is_pdf(file):
                text = scan_pdf(file, ocr)
            else:
                text = extract_text(file)

            results.update({entry.name: search_for_pii(text)}) 
            print("-"*TERM_WIDTH)

    with open("output.json", 'w') as file:
        json.dump(results, file, indent=4)
