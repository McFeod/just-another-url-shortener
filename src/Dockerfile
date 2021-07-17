FROM python:3.9-slim-buster

ARG API_PORT
ARG POETRY_VERSION

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /code

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/

RUN poetry install

COPY . /code/

EXPOSE ${API_PORT}
ENV PORT ${API_PORT}
