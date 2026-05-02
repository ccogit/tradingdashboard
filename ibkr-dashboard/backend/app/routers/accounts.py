from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID
from app.deps import get_current_user, get_db
from app.models.user import User
from app.models.account import Account

router = APIRouter()


@router.get("/accounts")
async def list_accounts(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.exec(select(Account).where(Account.user_id == user.id, Account.is_active == True))
    return [{"id": str(a.id), "ib_account_id": a.ib_account_id, "alias": a.alias, "currency": a.currency, "type": a.type} for a in result.all()]


@router.get("/accounts/{account_id}")
async def get_account(
    account_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.exec(select(Account).where(Account.id == account_id, Account.user_id == user.id))
    account = result.first()
    if not account:
        raise HTTPException(404, "Account not found")
    return {"id": str(account.id), "ib_account_id": account.ib_account_id, "alias": account.alias, "currency": account.currency, "type": account.type}
