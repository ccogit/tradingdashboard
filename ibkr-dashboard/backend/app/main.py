from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import get_settings
from app.exceptions import AppException, app_exception_handler
from app.logging_config import configure_logging
from app.db.session import engine
from sqlmodel import SQLModel

from app.routers import health, auth, accounts, portfolio, orders, contracts, market, copilot, settings as settings_router, ws as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    settings = get_settings()

    # Create tables (dev convenience; use alembic in prod)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Start IB Gateway client
    from app.services.ib_gateway import ib_client
    await ib_client.connect(settings.ib_gateway_host, settings.ib_gateway_port, settings.ib_client_id)

    # Start background workers
    import asyncio
    from app.workers.ib_event_pump import start_event_pump
    from app.workers.snapshot_loop import start_snapshot_loop
    pump_task = asyncio.create_task(start_event_pump())
    snapshot_task = asyncio.create_task(start_snapshot_loop())

    yield

    # Shutdown
    pump_task.cancel()
    snapshot_task.cancel()
    await ib_client.disconnect()
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="IBKR Dashboard API", version="1.0.0", lifespan=lifespan)

    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppException, app_exception_handler)

    prefix = "/api/v1"
    app.include_router(health.router, prefix=prefix, tags=["health"])
    app.include_router(auth.router, prefix=prefix, tags=["auth"])
    app.include_router(accounts.router, prefix=prefix, tags=["accounts"])
    app.include_router(portfolio.router, prefix=prefix, tags=["portfolio"])
    app.include_router(orders.router, prefix=prefix, tags=["orders"])
    app.include_router(contracts.router, prefix=prefix, tags=["contracts"])
    app.include_router(market.router, prefix=prefix, tags=["market"])
    app.include_router(copilot.router, prefix=prefix, tags=["copilot"])
    app.include_router(settings_router.router, prefix=prefix, tags=["settings"])
    app.include_router(ws_router.router, tags=["websocket"])

    return app


app = create_app()
