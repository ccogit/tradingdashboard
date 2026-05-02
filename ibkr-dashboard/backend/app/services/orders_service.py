from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.order import Order
from app.models.user import User
from app.schemas.orders import OrderCreate, OrderRead, WhatIfResult
from app.services.ib_orders import place_order, cancel_ib_order, what_if_order
from app.utils.ids import new_uuid, client_order_id
from app.utils.time import utcnow
import logging

logger = logging.getLogger(__name__)


async def create_order(body: OrderCreate, user: User, db: AsyncSession, ib_client) -> OrderRead:
    coid = body.client_order_id or client_order_id()
    order = Order(
        id=new_uuid(),
        account_id=UUID(body.account_id),
        user_id=user.id,
        client_order_id=coid,
        conid=body.conid or 0,
        symbol=body.symbol or "",
        sec_type=body.sec_type or "STK",
        exchange=body.exchange or "SMART",
        currency=body.currency or "USD",
        side=body.side,
        quantity=body.quantity,
        order_type=body.order_type,
        limit_price=body.limit_price,
        tif=body.tif,
        outside_rth=body.outside_rth,
        status="pending",
    )
    db.add(order)
    await db.commit()

    try:
        result = await place_order(body, ib_client)
        order.ib_order_id = result["ib_order_id"]
        order.conid = result.get("conid", order.conid)
        order.status = "submitted"
    except Exception as e:
        order.status = "rejected"
        order.reject_reason = str(e)
        logger.error(f"Order placement failed: {e}")

    order.updated_at = utcnow()
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return _to_read(order)


async def preview_order(body: OrderCreate, ib_client) -> WhatIfResult:
    return await what_if_order(body, ib_client)


async def list_orders(account_id: str, status: str | None, db: AsyncSession) -> list[OrderRead]:
    q = select(Order).where(Order.account_id == UUID(account_id))
    if status:
        q = q.where(Order.status == status)
    result = await db.exec(q.order_by(Order.created_at.desc()))
    return [_to_read(o) for o in result.all()]


async def cancel_order(order_id: UUID, user: User, db: AsyncSession, ib_client) -> OrderRead:
    result = await db.exec(select(Order).where(Order.id == order_id, Order.user_id == user.id))
    order = result.first()
    if not order:
        from fastapi import HTTPException
        raise HTTPException(404, "Order not found")
    if order.ib_order_id:
        await cancel_ib_order(order.ib_order_id, ib_client)
    order.status = "cancelled"
    order.updated_at = utcnow()
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return _to_read(order)


def _to_read(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        client_order_id=order.client_order_id,
        ib_order_id=order.ib_order_id,
        account_id=str(order.account_id),
        conid=order.conid,
        symbol=order.symbol,
        side=order.side,
        quantity=float(order.quantity),
        order_type=order.order_type,
        limit_price=float(order.limit_price) if order.limit_price else None,
        tif=order.tif,
        outside_rth=order.outside_rth,
        status=order.status,
        filled_quantity=float(order.filled_quantity),
        avg_fill_price=float(order.avg_fill_price) if order.avg_fill_price else None,
        commission=float(order.commission) if order.commission else None,
        reject_reason=order.reject_reason,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )
