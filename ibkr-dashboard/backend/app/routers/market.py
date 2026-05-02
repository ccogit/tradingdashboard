from fastapi import APIRouter, Depends, Query
from app.deps import get_current_user
from app.models.user import User
from app.services.ib_market_data import get_snapshot_quote
from app.services.ib_gateway import ib_client

router = APIRouter()


@router.get("/market/quote/{conid}")
async def quote(
    conid: int,
    user: User = Depends(get_current_user),
):
    return await get_snapshot_quote(conid, ib_client)


@router.get("/market/bars")
async def bars(
    conid: int = Query(...),
    duration: str = Query("1 D"),
    bar_size: str = Query("1 min"),
    what_to_show: str = Query("TRADES"),
    user: User = Depends(get_current_user),
):
    from app.services.ib_market_data import get_bars
    return await get_bars(conid, duration, bar_size, what_to_show, ib_client)
