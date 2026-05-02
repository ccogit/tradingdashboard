from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.deps import get_current_user, get_db
from app.models.user import User
from app.utils.time import utcnow

router = APIRouter()


@router.get("/settings")
async def get_settings_endpoint(user: User = Depends(get_current_user)):
    return {"trading_mode": user.trading_mode, "default_account_id": str(user.default_account_id) if user.default_account_id else None}


@router.put("/settings")
async def update_settings(
    body: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if "trading_mode" in body:
        user.trading_mode = body["trading_mode"]
    user.updated_at = utcnow()
    db.add(user)
    await db.commit()
    return {"trading_mode": user.trading_mode}
