import uuid
from datetime import datetime, timezone


def new_uuid() -> uuid.UUID:
    return uuid.uuid4()


def client_order_id() -> str:
    ts = int(datetime.now(timezone.utc).timestamp() * 1000)
    return f"co-{ts}-{uuid.uuid4().hex[:8]}"
