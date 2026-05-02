import asyncio
from app.schemas.orders import OrderCreate, WhatIfResult
import logging

logger = logging.getLogger(__name__)


async def place_order(body: OrderCreate, ib_client) -> dict:
    from ib_async import Contract, Order as IBOrder, Stock
    contract = Contract(
        conId=body.conid,
        symbol=body.symbol or "",
        secType=body.sec_type or "STK",
        exchange=body.exchange or "SMART",
        currency=body.currency or "USD",
    )
    if body.conid:
        await ib_client.ib.qualifyContractsAsync(contract)
    else:
        contracts = await ib_client.ib.qualifyContractsAsync(
            Stock(body.symbol, body.exchange or "SMART", body.currency or "USD")
        )
        contract = contracts[0]

    order = IBOrder()
    order.action = body.side
    order.totalQuantity = body.quantity
    order.orderType = body.order_type
    if body.order_type == "LMT" and body.limit_price:
        order.lmtPrice = body.limit_price
    order.tif = body.tif
    order.outsideRth = body.outside_rth

    trade = ib_client.ib.placeOrder(contract, order)
    return {"ib_order_id": trade.order.orderId, "ib_perm_id": trade.order.permId, "conid": contract.conId}


async def cancel_ib_order(ib_order_id: int, ib_client) -> None:
    from ib_async import Order as IBOrder
    order = IBOrder()
    order.orderId = ib_order_id
    ib_client.ib.cancelOrder(order)


async def what_if_order(body: OrderCreate, ib_client) -> WhatIfResult:
    from ib_async import Contract, Order as IBOrder, Stock
    contract = Stock(body.symbol or "", body.exchange or "SMART", body.currency or "USD")
    contracts = await ib_client.ib.qualifyContractsAsync(contract)
    contract = contracts[0]

    order = IBOrder()
    order.action = body.side
    order.totalQuantity = body.quantity
    order.orderType = body.order_type
    if body.order_type == "LMT" and body.limit_price:
        order.lmtPrice = body.limit_price
    order.whatIf = True

    trade = ib_client.ib.placeOrder(contract, order)
    await asyncio.sleep(1)
    state = trade.orderStatus

    return WhatIfResult(
        initial_margin=float(state.initMarginChange or 0),
        maintenance_margin=float(state.maintMarginChange or 0),
        equity_with_loan=float(state.equityWithLoanChange or 0),
        commission=float(state.commission or 0),
        currency="USD",
    )
