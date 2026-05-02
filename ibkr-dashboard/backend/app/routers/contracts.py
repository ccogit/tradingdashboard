from fastapi import APIRouter, Depends, Query
from app.deps import get_current_user
from app.models.user import User
from app.services.ib_contracts import search_contracts, get_contract

router = APIRouter()


@router.get("/contracts/search")
async def search(
    q: str = Query(..., min_length=1),
    sec_type: str = Query(None),
    user: User = Depends(get_current_user),
):
    from app.services.ib_gateway import ib_client
    return await search_contracts(q, sec_type, ib_client)


@router.get("/contracts/{conid}")
async def get(
    conid: int,
    user: User = Depends(get_current_user),
):
    from app.services.ib_gateway import ib_client
    return await get_contract(conid, ib_client)
