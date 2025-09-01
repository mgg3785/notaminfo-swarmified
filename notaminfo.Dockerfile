FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apk add --no-cache \
    mariadb-client \
    mariadb-connector-c-dev \
    mariadb-dev \
    pkgconfig \
    gcc \
    musl-dev \
    linux-headers

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]