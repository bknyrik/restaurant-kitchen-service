FROM python:3.12-alpine3.24
LABEL maintainer="knyrikkolesnichenko2004@gmail.com";

COPY . .

WORKDIR /flask-app

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=2.4.1

RUN pip install poetry && poetry install --no-root
