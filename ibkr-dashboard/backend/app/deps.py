from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import async_session
from app.core.security import ClerkJWTVerifier
from app.models.user import User
from app.models.account import Account
from sqlmodel import select

bearer_scheme = HTTPBearer()
jwt_verifier = ClerkJWTVerifier()


async def get_db():
    async with async_session() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    claims = await jwt_verifier.verify(credentials.credentials)
    clerk_user_id = claims["sub"]

    result = await db.exec(select(User).where(User.clerk_user_id == clerk_user_id))
    user = result.first()
    if not user:
        user = User(
            clerk_user_id=clerk_user_id,
            email=claims.get("email", ""),
            name=claims.get("name"),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user


async def get_ib():
    from app.services.ib_gateway import ib_client
    if not ib_client.is_connected:
        from app.exceptions import IBNotConnectedError
        raise IBNotConnectedError()
    return ib_client
