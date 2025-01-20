FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /app/

ENV PIPENV_CUSTOM_VENV_NAME=extract
RUN pip install --no-cache-dir pipenv && pipenv install --deploy

COPY . /app

RUN pipenv run pytest

EXPOSE 8000

CMD ["pipenv", "run", "fastapi", "run"]