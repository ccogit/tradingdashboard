# Stage 1: build Python deps
FROM python:3.12-slim AS pybuilder
WORKDIR /build
RUN pip install uv
COPY ../backend/pyproject.toml .
RUN uv pip install --system -e . 2>/dev/null; pip install fastapi uvicorn sqlmodel asyncpg alembic pydantic-settings anthropic httpx python-jose cachetools python-multipart ib-async

# Stage 2: combined runtime
FROM ghcr.io/gnzsnz/ib-gateway:stable

# Install Python 3.12 alongside the existing IB Gateway
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-dev python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=pybuilder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=pybuilder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=pybuilder /usr/local/bin/alembic /usr/local/bin/alembic

# Copy backend source
WORKDIR /backend
COPY ../backend/ .

# Verify IB Gateway startup script exists (fail fast at build time)
RUN test -f /home/ibgateway/scripts/run.sh || \
    (echo "ERROR: /home/ibgateway/scripts/run.sh not found in base image" && exit 1)

# Startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

ENTRYPOINT ["/start.sh"]
