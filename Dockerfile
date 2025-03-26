FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt update && apt install -y \
    mariadb-client \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    musl-dev
    
RUN uv sync


CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]