import logging
from app.schemas.portfolio import PortfolioSummary, PositionDTO
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


async def get_account_summary(account_id: str, ib_client) -> dict:
    summary = await ib_client.ib.reqAccountSummaryAsync()
    values = {item.tag: item.value for item in summary if item.account == account_id or not account_id}
    return values


async def get_portfolio_positions(account_id: str, ib_client) -> list[PositionDTO]:
    portfolio = ib_client.ib.portfolio(account_id) if account_id else ib_client.ib.portfolio()
    positions = []
    for item in portfolio:
        positions.append(PositionDTO(
            account_id=item.account,
            conid=item.contract.conId,
            symbol=item.contract.symbol,
            sec_type=item.contract.secType,
            exchange=item.contract.exchange or "SMART",
            currency=item.contract.currency,
            quantity=float(item.position),
            avg_cost=float(item.averageCost),
            market_price=float(item.marketPrice),
            market_value=float(item.marketValue),
            unrealized_pnl=float(item.unrealizedPNL),
            realized_pnl=float(item.realizedPNL),
            day_pnl=0.0,
            pct_of_nav=0.0,
        ))
    return positions
