FROM python:3.11

# Instala pdftotext (Poppler utils)
RUN apt-get update && apt-get install -y poppler-utils

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
