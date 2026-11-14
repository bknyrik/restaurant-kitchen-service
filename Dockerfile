FROM python:3.12-alpine3.24
LABEL maintainer="knyrikkolesnichenko2004@gmail.com";

WORKDIR /flask-app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN pip install poetry && poetry install --no-root --without dev

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
