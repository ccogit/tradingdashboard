import time
from typing import Any
import httpx
from jose import jwt, JWTError
from cachetools import TTLCache
from app.config import get_settings
from fastapi import HTTPException


class ClerkJWTVerifier:
    def __init__(self):
        self._jwks_cache: TTLCache = TTLCache(maxsize=1, ttl=3600)

    async def _get_jwks(self) -> dict:
        if "jwks" in self._jwks_cache:
            return self._jwks_cache["jwks"]
        settings = get_settings()
        async with httpx.AsyncClient() as client:
            resp = await client.get(settings.clerk_jwks_url)
            resp.raise_for_status()
            jwks = resp.json()
        self._jwks_cache["jwks"] = jwks
        return jwks

    async def verify(self, token: str) -> dict[str, Any]:
        settings = get_settings()
        try:
            jwks = await self._get_jwks()
            claims = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                audience=settings.clerk_audience,
                issuer=settings.clerk_issuer,
            )
            return claims
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
