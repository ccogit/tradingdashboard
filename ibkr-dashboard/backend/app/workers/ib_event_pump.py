import asyncio
import logging
from app.core.events import event_bus

logger = logging.getLogger(__name__)


async def start_event_pump() -> None:
    from app.services.ib_gateway import ib_client
    logger.info("IB event pump started")
    try:
        while True:
            if ib_client.is_connected and ib_client.ib:
                ib = ib_client.ib
                ib.orderStatusEvent += _on_order_status
                ib.execDetailsEvent += _on_exec_details
                ib.accountValueEvent += _on_account_value
                ib.pnlEvent += _on_pnl
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.info("IB event pump stopped")


def _on_order_status(trade) -> None:
    asyncio.create_task(event_bus.publish("order_status", {
        "ib_order_id": trade.order.orderId,
        "status": trade.orderStatus.status,
        "filled": trade.orderStatus.filled,
        "avg_fill_price": trade.orderStatus.avgFillPrice,
    }))


def _on_exec_details(trade, fill) -> None:
    asyncio.create_task(event_bus.publish("execution", {
        "exec_id": fill.execution.execId,
        "symbol": trade.contract.symbol,
        "side": fill.execution.side,
        "quantity": fill.execution.shares,
        "price": fill.execution.price,
    }))


def _on_account_value(value) -> None:
    asyncio.create_task(event_bus.publish("account_value", {
        "key": value.tag,
        "value": value.value,
        "currency": value.currency,
        "account_id": value.account,
    }))


def _on_pnl(pnl) -> None:
    asyncio.create_task(event_bus.publish("pnl", {
        "daily_pnl": pnl.dailyPnL,
        "unrealized_pnl": pnl.unrealizedPnL,
        "realized_pnl": pnl.realizedPnL,
    }))
