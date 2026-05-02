FROM ghcr.io/gnzsnz/ib-gateway:stable

# Healthcheck: TCP connect to paper trading port
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=5 \
  CMD nc -z localhost 4002 || exit 1
