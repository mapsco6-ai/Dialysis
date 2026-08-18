# Multi-stage build: keep the runtime image free of compilers/build tools.
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install --no-cache-dir --prefix=/install -r requirements/prod.txt


FROM python:3.11-slim AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash dialysis

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

RUN mkdir -p /app/staticfiles /app/media \
    && chmod +x /app/deploy/entrypoint.sh \
    && chown -R dialysis:dialysis /app

USER dialysis

ENV DJANGO_SETTINGS_MODULE=config.settings.prod \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
