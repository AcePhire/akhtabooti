import sys
from unstructured.partition.auto import partition

filename = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) > 2 else "eng"

elements = partition(filename=filename, strategy="auto", include_page_breaks=True, languages=[lang])

text = "\n\n".join([str(element) for element in elements])

print(text)
