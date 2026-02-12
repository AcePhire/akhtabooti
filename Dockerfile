FROM python:3.14.1-trixie

RUN apt-get update && \ 
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get install -y tesseract-ocr

RUN pip install --upgrade pip
RUN pip install unstructured && \
    pip install unstructured[all-docs]
