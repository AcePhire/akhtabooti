# Akhtabooti

Akhtabooti is a Personally Identifiable Information (PII) scanner that uses Optical Character Recognition (OCR) and regular expression to search for Goverment IDs, Passports, emails, and phones in images, PDFs, and documents.

## Usage
#### Prerequisites:
- Python
- pip
#### Installation
**1. Clone the repository:**
```
git clone git@github.com:AcePhire/akhtabooti.git
cd akhtabooti
```
**2. Install dependencies:**

```
pip install -r requirements.txt
```
**3. Run akhtabooti:**

```
python akhtabooit.py <directory to scan>
```
A file named `output.json` is created in the scanned directory, containing output from the tool.

---
### Docker
You can also run akhtabooti in a Docker container:
```
# Build the image
docker build -t akhtabooti .

# Run the container
docker run -v <directory to scan>:/pii akhtabooti
```
