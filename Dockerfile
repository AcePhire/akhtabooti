FROM python:3.14.1-trixie

COPY . .

RUN apt-get update && \ 
    apt-get install -y ffmpeg libsm6 libxext6

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "akhtabooti.py", "/pii"]
