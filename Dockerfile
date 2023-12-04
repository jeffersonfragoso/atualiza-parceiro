FROM python:3.11.4-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=10000 \
  POETRY_VERSION=1.6.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  POETRY_VIRTUALENVS_IN_PROJECT=0 \
  POETRY_VIRTUALENVS_CREATE=0

# install system dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends build-essential gcc && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  pip install "poetry==$POETRY_VERSION"

# instala dependencias do app
FROM base AS dependencies_stage
WORKDIR /tmp
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# configura usuário app e arquivos para execução
FROM dependencies_stage as runtime
RUN mkdir -p /home/poc_pdtec
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /home/poc_pdtec
USER app
WORKDIR /home/poc_pdtec/
COPY . /home/poc_pdtec/
ENV PYTHONPATH=${PYTHONPATH}/home/poc_pdtec/src
