# Stage 1: install Python packages
FROM python:3.12-slim AS pybuilder
WORKDIR /build
RUN pip install uv
COPY backend/pyproject.toml .
RUN uv pip install --system -e . 2>/dev/null; \
    pip install fastapi uvicorn sqlmodel asyncpg alembic pydantic-settings \
                anthropic httpx python-jose cachetools python-multipart ib-async

# Stage 2: pull IB Gateway image to extract its files
FROM ghcr.io/gnzsnz/ib-gateway:stable AS gateway-source

# Stage 3: final image — Python 3.12 slim with Java + IB Gateway files
FROM python:3.12-slim

# Java runtime + Xvfb (IB Gateway headless GUI) + nc (health check in start.sh)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    xvfb \
    x11-utils \
    libxtst6 \
    libxi6 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Recreate the user that IB Gateway scripts expect
RUN useradd -m -s /bin/bash ibgateway

# Copy the full IB Gateway installation from the official image
COPY --from=gateway-source /home/ibgateway /home/ibgateway
RUN chown -R ibgateway:ibgateway /home/ibgateway

# Copy Python packages and CLI tools from pybuilder
COPY --from=pybuilder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=pybuilder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=pybuilder /usr/local/bin/alembic /usr/local/bin/alembic

# Copy backend source
WORKDIR /backend
COPY backend/ .

# Verify IB Gateway startup script exists (fail fast at build time)
RUN test -f /home/ibgateway/scripts/run.sh || \
    (echo "ERROR: /home/ibgateway/scripts/run.sh not found in gateway image" && exit 1)

COPY combined/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000
ENTRYPOINT ["/start.sh"]
