from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings

settings = get_settings()


def _build_engine_args(url: str) -> tuple[str, dict]:
    # asyncpg does not accept libpq's `sslmode`; strip it from the URL and
    # translate into the asyncpg `ssl` connect_arg.
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    sslmode = query.pop("sslmode", [None])[0]
    clean_url = urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
    connect_args: dict = {}
    if sslmode in ("require", "verify-ca", "verify-full"):
        connect_args["ssl"] = True
    return clean_url, connect_args


_url, _connect_args = _build_engine_args(settings.database_url)
engine = create_async_engine(_url, echo=False, connect_args=_connect_args)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
