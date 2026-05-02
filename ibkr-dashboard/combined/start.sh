#!/bin/bash
set -e

echo "==> Starting IB Gateway..."
/home/ibgateway/scripts/run.sh &

# Wait up to 120s for the gateway port to open
GATEWAY_PORT=${IB_GATEWAY_PORT:-4002}
echo "==> Waiting for IB Gateway on port $GATEWAY_PORT..."
for i in $(seq 1 24); do
  if nc -z localhost "$GATEWAY_PORT" 2>/dev/null; then
    echo "==> IB Gateway ready after $((i * 5))s"
    break
  fi
  sleep 5
done

if ! nc -z localhost "$GATEWAY_PORT" 2>/dev/null; then
  echo "WARNING: IB Gateway not ready after 120s, starting backend anyway"
fi

echo "==> Running database migrations..."
cd /backend
alembic upgrade head || echo "WARNING: migration failed, continuing"

echo "==> Starting FastAPI backend..."
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}" \
  --proxy-headers \
  --forwarded-allow-ips="*"
