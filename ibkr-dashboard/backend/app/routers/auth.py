from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.deps import get_current_user, get_db
from app.models.user import User
from app.models.account import Account

router = APIRouter()


@router.get("/me")
async def me(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.exec(select(Account).where(Account.user_id == user.id))
    accounts = result.all()
    return {
        "id": str(user.id),
        "clerk_user_id": user.clerk_user_id,
        "email": user.email,
        "name": user.name,
        "trading_mode": user.trading_mode,
        "accounts": [
            {
                "id": str(a.id),
                "ib_account_id": a.ib_account_id,
                "alias": a.alias,
                "currency": a.currency,
                "type": a.type,
            }
            for a in accounts
        ],
    }
