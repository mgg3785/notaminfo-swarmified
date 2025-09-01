FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
# RUN apk add --no-cache \
#     mariadb-client \
#     mariadb-connector-c-dev \
#     mariadb-dev \
#     pkgconfig \
#     gcc \
#     musl-dev \
#     linux-headers

RUN pip install -no-cache-dir uv && uv sync

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]