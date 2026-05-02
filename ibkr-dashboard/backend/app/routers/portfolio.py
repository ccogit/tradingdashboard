from fastapi import APIRouter, Depends, Query
from app.deps import get_current_user, get_db
from app.models.user import User
from app.services.portfolio_service import get_portfolio_summary, get_positions, get_pnl_history

router = APIRouter()


@router.get("/portfolio/summary")
async def portfolio_summary(
    account_id: str = Query(...),
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    return await get_portfolio_summary(account_id, db)


@router.get("/portfolio/positions")
async def positions(
    account_id: str = Query(...),
    user: User = Depends(get_current_user),
):
    return await get_positions(account_id)


@router.get("/portfolio/pnl")
async def pnl(
    account_id: str = Query(...),
    range: str = Query("1d"),
    user: User = Depends(get_current_user),
    db=Depends(get_db),
):
    return await get_pnl_history(account_id, range, db)
