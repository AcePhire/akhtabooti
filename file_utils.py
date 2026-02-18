from unstructured.partition.auto import partition
from PIL import Image
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

# Extract file from documents
def extract_text(file_path):
    elements = partition(filename=file_path, strategy="auto", include_page_breaks=True)

    return "\n".join([str(element) for element in elements])
