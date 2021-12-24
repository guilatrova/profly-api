FROM python:3.9-slim-buster as poetry-base

ENV \
  # Python env vars
  # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
  PYTHONUNBUFFERED=1 \
  # Pip env vars (https://pip.pypa.io/en/stable/user_guide/#environment-variables)
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry env vars (https://python-poetry.org/docs/configuration/#using-environment-variables)
  POETRY_VERSION=1.1.12 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

RUN mkdir /app
WORKDIR /app

FROM poetry-base as base-deps

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev

FROM base-deps as prod

COPY src/ /app/

ARG COMMIT_HASH
ENV COMMIT_HASH=$COMMIT_HASH

CMD ["gunicorn",  "profly.wsgi", "--bind", ":8080", "--worker-class", "gevent", "--worker-connections", "300", "--workers", "3"]

FROM prod as dev

RUN pip install virtualenv && poetry install

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]

EXPOSE 8080
