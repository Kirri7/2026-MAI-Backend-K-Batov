FROM python:3.14-slim

WORKDIR /app # TODO ???

# psycopg зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install  --no-cache-dir -r requirements.txt

# Весь (почти) Django-проект будет скопирован
COPY project/ .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "project.wsgi:application"]

# TODO entrypoint?