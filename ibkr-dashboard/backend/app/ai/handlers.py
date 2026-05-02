from typing import Any
from app.services.portfolio_service import get_portfolio_summary, get_positions
from app.services.orders_service import list_orders
from app.services.ib_contracts import search_contracts
from app.services.ib_market_data import get_snapshot_quote
from app.services.ib_gateway import ib_client
from app.schemas.orders import OrderCreate


async def handle_get_portfolio_summary(args: dict, ctx: dict) -> dict:
    account_id = args.get("account_id") or ctx["account_id"]
    summary = await get_portfolio_summary(account_id, ctx["db"])
    return summary.model_dump()


async def handle_get_positions(args: dict, ctx: dict) -> dict:
    account_id = args.get("account_id") or ctx["account_id"]
    positions = await get_positions(account_id)
    symbol_filter = args.get("symbol_filter", "").upper()
    if symbol_filter:
        positions = [p for p in positions if symbol_filter in p.symbol.upper()]
    return {"positions": [p.model_dump() for p in positions]}


async def handle_get_open_orders(args: dict, ctx: dict) -> dict:
    account_id = args.get("account_id") or ctx["account_id"]
    orders = await list_orders(account_id, "working", ctx["db"])
    return {"orders": [o.model_dump() for o in orders]}


async def handle_search_contract(args: dict, ctx: dict) -> dict:
    results = await search_contracts(args["query"], args.get("sec_type"), ib_client)
    return {"contracts": [r.model_dump() for r in results]}


async def handle_get_quote(args: dict, ctx: dict) -> dict:
    conid = args.get("conid")
    if not conid and args.get("symbol"):
        results = await search_contracts(args["symbol"], args.get("sec_type", "STK"), ib_client)
        if results:
            conid = results[0].conid
    if not conid:
        return {"error": "Could not resolve contract"}
    quote = await get_snapshot_quote(conid, ib_client)
    return quote.model_dump()


async def handle_preview_order(args: dict, ctx: dict) -> dict:
    from app.services.ib_orders import what_if_order
    body = OrderCreate(
        account_id=args.get("account_id") or ctx["account_id"],
        symbol=args.get("symbol"),
        sec_type=args.get("sec_type", "STK"),
        exchange=args.get("exchange", "SMART"),
        currency=args.get("currency", "USD"),
        side=args["side"],
        quantity=args["quantity"],
        order_type=args["order_type"],
        limit_price=args.get("limit_price"),
        tif=args.get("tif", "DAY"),
    )
    result = await what_if_order(body, ib_client)
    return result.model_dump()


async def handle_stage_order(args: dict, ctx: dict) -> dict:
    order = OrderCreate(
        account_id=args.get("account_id") or ctx["account_id"],
        symbol=args.get("symbol"),
        sec_type=args.get("sec_type", "STK"),
        exchange=args.get("exchange", "SMART"),
        currency=args.get("currency", "USD"),
        side=args["side"],
        quantity=args["quantity"],
        order_type=args["order_type"],
        limit_price=args.get("limit_price"),
        tif=args.get("tif", "DAY"),
    )
    return {"staged": True, "order": order.model_dump(), "rationale": args.get("rationale", "")}


async def handle_cancel_order(args: dict, ctx: dict) -> dict:
    from uuid import UUID
    from app.services.orders_service import cancel_order
    result = await cancel_order(UUID(args["order_id"]), ctx["user"], ctx["db"], ib_client)
    return result.model_dump()


HANDLERS = {
    "get_portfolio_summary": handle_get_portfolio_summary,
    "get_positions": handle_get_positions,
    "get_open_orders": handle_get_open_orders,
    "search_contract": handle_search_contract,
    "get_quote": handle_get_quote,
    "preview_order": handle_preview_order,
    "stage_order": handle_stage_order,
    "cancel_order": handle_cancel_order,
}
