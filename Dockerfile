FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN /root/.local/bin/poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 80

# CMD ["/root/.local/bin/poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--access-logfile=/var/log/access.log", "gunicorn_test.app:app"]
