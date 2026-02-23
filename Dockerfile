FROM python:3.11-slim

# Prevent python buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install system deps (needed for pdf + psycopg)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# copy requirements first (docker cache optimization)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
