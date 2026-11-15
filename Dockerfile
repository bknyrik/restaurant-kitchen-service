FROM python:3.12-alpine3.24
LABEL maintainer="knyrikkolesnichenko2004@gmail.com";


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

EXPOSE 8000

WORKDIR /flask-app

RUN pip install poetry

COPY poetry.lock /flask-app/poetry.lock
COPY pyproject.toml /flask-app/pyproject.toml

RUN poetry install --without dev --no-root

COPY . /flask-app

CMD sh -c "poetry run flask db upgrade && poetry run flask run"
