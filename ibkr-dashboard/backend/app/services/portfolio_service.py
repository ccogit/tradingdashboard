from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from datetime import datetime, timedelta, timezone
from app.schemas.portfolio import PortfolioSummary, PositionDTO, PnLHistory, PnLPoint
from app.services.ib_account import get_account_summary, get_portfolio_positions
from app.services.ib_gateway import ib_client
from app.models.pnl_snapshot import AccountPnLSnapshot


async def get_portfolio_summary(account_id: str, db: AsyncSession) -> PortfolioSummary:
    values = await get_account_summary(account_id, ib_client)
    positions = await get_portfolio_positions(account_id, ib_client)
    return PortfolioSummary(
        account_id=account_id,
        net_liquidation=float(values.get("NetLiquidation", 0)),
        total_cash=float(values.get("TotalCashValue", 0)),
        buying_power=float(values.get("BuyingPower", 0)),
        excess_liquidity=float(values.get("ExcessLiquidity", 0)),
        maintenance_margin=float(values.get("MaintMarginReq", 0)),
        day_pnl=float(values.get("DayTradesRemaining", 0)),
        unrealized_pnl=float(values.get("UnrealizedPnL", 0)),
        realized_pnl=float(values.get("RealizedPnL", 0)),
        positions_count=len(positions),
        as_of=datetime.now(timezone.utc),
    )


async def get_positions(account_id: str) -> list[PositionDTO]:
    return await get_portfolio_positions(account_id, ib_client)


async def get_pnl_history(account_id: str, range_str: str, db: AsyncSession) -> PnLHistory:
    now = datetime.now(timezone.utc)
    range_map = {"1d": timedelta(days=1), "1w": timedelta(weeks=1), "1m": timedelta(days=30), "ytd": timedelta(days=365)}
    since = now - range_map.get(range_str, timedelta(days=1))

    result = await db.exec(
        select(AccountPnLSnapshot)
        .where(AccountPnLSnapshot.snapshot_at >= since)
        .order_by(AccountPnLSnapshot.snapshot_at)
    )
    snapshots = result.all()
    points = [PnLPoint(ts=s.snapshot_at, equity=float(s.net_liquidation), pnl=float(s.daily_pnl)) for s in snapshots]
    return PnLHistory(points=points)
