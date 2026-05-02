from fastapi import APIRouter, Depends
from app.services.ib_gateway import ib_client

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/health/ib")
async def health_ib():
    return {
        "connected": ib_client.is_connected,
        "host": ib_client.host,
        "port": ib_client.port,
        "client_id": ib_client.client_id,
        "last_error": ib_client.last_error,
    }
