FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apk add --no-cache \
    pkgconfig \
    gcc \
    musl-dev \
    linux-headers

RUN pip install --no-cache-dir uv
RUN uv sync
RUN uv pip install psycopg[binary]

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]