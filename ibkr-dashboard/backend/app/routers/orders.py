from fastapi import APIRouter, Depends, Query
from uuid import UUID
from app.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.orders import OrderCreate
from app.services.orders_service import create_order, preview_order, list_orders, cancel_order

router = APIRouter()


@router.post("/orders/preview")
async def preview(
    body: OrderCreate,
    user: User = Depends(get_current_user),
    ib=Depends(lambda: None),
):
    from app.services.ib_gateway import ib_client
    return await preview_order(body, ib_client)


@router.post("/orders")
async def place_order(
    body: OrderCreate,
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    from app.services.ib_gateway import ib_client
    return await create_order(body, user, db, ib_client)


@router.get("/orders")
async def get_orders(
    account_id: str = Query(...),
    status: str = Query(None),
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    return await list_orders(account_id, status, db)


@router.delete("/orders/{order_id}")
async def cancel(
    order_id: UUID,
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    from app.services.ib_gateway import ib_client
    return await cancel_order(order_id, user, db, ib_client)
