FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install postgresql-client
RUN pip install --no-cache-dir uv
RUN uv sync
RUN uv pip install psycopg[binary]

RUN chmod +x /app/django-entry.sh
ENTRYPOINT ["/app/django-entry.sh"]