import asyncio
import logging
from datetime import datetime, timezone
from app.config import get_settings
from app.db.session import async_session
from app.models.pnl_snapshot import AccountPnLSnapshot
from app.utils.ids import new_uuid

logger = logging.getLogger(__name__)


async def start_snapshot_loop() -> None:
    settings = get_settings()
    logger.info("Snapshot loop started")
    try:
        while True:
            await asyncio.sleep(settings.snapshot_interval_seconds)
            await _take_snapshot()
    except asyncio.CancelledError:
        logger.info("Snapshot loop stopped")


async def _take_snapshot() -> None:
    from app.services.ib_gateway import ib_client
    if not ib_client.is_connected:
        return
    settings = get_settings()
    try:
        from app.services.ib_account import get_account_summary
        values = await get_account_summary(settings.ib_account_id, ib_client)
        snapshot = AccountPnLSnapshot(
            id=new_uuid(),
            account_id=new_uuid(),
            net_liquidation=float(values.get("NetLiquidation", 0)),
            total_cash=float(values.get("TotalCashValue", 0)),
            buying_power=float(values.get("BuyingPower", 0)),
            excess_liquidity=float(values.get("ExcessLiquidity", 0)),
            daily_pnl=float(values.get("DayTradesRemaining", 0)),
            unrealized_pnl=float(values.get("UnrealizedPnL", 0)),
            realized_pnl=float(values.get("RealizedPnL", 0)),
            snapshot_at=datetime.now(timezone.utc),
        )
        async with async_session() as db:
            db.add(snapshot)
            await db.commit()
    except Exception as e:
        logger.warning(f"Snapshot failed: {e}")
