import asyncio
from datetime import datetime, timezone
from typing import Optional
from app.schemas.market import QuoteTick, BarDTO
from app.core.events import event_bus
import logging

logger = logging.getLogger(__name__)
_subscriptions: dict[int, int] = {}


async def subscribe_market_data(conid: int, ib_client) -> None:
    if conid in _subscriptions:
        _subscriptions[conid] += 1
        return
    _subscriptions[conid] = 1
    try:
        from ib_async import Contract
        contract = Contract(conId=conid)
        await ib_client.ib.qualifyContractsAsync(contract)
        ticker = ib_client.ib.reqMktData(contract)
        ticker.updateEvent += lambda t: asyncio.create_task(_on_tick(conid, t))
    except Exception as e:
        logger.warning(f"Failed to subscribe to market data for {conid}: {e}")
        _subscriptions.pop(conid, None)


async def _on_tick(conid: int, ticker) -> None:
    tick = QuoteTick(
        conid=conid,
        bid=ticker.bid if ticker.bid and ticker.bid > 0 else None,
        ask=ticker.ask if ticker.ask and ticker.ask > 0 else None,
        last=ticker.last if ticker.last and ticker.last > 0 else None,
        bid_size=ticker.bidSize if ticker.bidSize else None,
        ask_size=ticker.askSize if ticker.askSize else None,
        volume=ticker.volume if ticker.volume else None,
        ts=datetime.now(timezone.utc),
    )
    await event_bus.publish("tick", tick)


async def get_snapshot_quote(conid: int, ib_client) -> QuoteTick:
    from ib_async import Contract
    contract = Contract(conId=conid)
    await ib_client.ib.qualifyContractsAsync(contract)
    tickers = await ib_client.ib.reqTickersAsync(contract)
    ticker = tickers[0] if tickers else None
    return QuoteTick(
        conid=conid,
        bid=getattr(ticker, "bid", None),
        ask=getattr(ticker, "ask", None),
        last=getattr(ticker, "last", None),
        ts=datetime.now(timezone.utc),
    )


async def get_bars(conid: int, duration: str, bar_size: str, what_to_show: str, ib_client) -> list[BarDTO]:
    from ib_async import Contract
    contract = Contract(conId=conid)
    await ib_client.ib.qualifyContractsAsync(contract)
    bars = await ib_client.ib.reqHistoricalDataAsync(
        contract,
        endDateTime="",
        durationStr=duration,
        barSizeSetting=bar_size,
        whatToShow=what_to_show,
        useRTH=True,
    )
    return [BarDTO(
        ts=b.date,
        open=b.open,
        high=b.high,
        low=b.low,
        close=b.close,
        volume=b.volume,
        wap=b.average,
        count=b.barCount,
    ) for b in bars]
