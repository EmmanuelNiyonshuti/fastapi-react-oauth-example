FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency files first
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

ENV PYTHONPATH=/app

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./


CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "8000"]
