FROM python:3.12.7-alpine3.20

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /ncc_backend

RUN apk update && \
    apk add --no-cache jq python3-dev build-base libpq-dev gcc

COPY Pipfile.lock .
RUN jq -r '.default | to_entries[] | .key + .value.version ' Pipfile.lock > requirements.txt && \
    pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]