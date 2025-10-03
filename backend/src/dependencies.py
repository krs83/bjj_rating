from fastapi import Depends, HTTPException, status
from typing import Annotated
import jwt

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from backend.src.config import settings
from backend.src.database import engine
from backend.src.models import User
from backend.src.models.token import TokenData

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access_token"
)
DPToken = Annotated[str, Depends(reusable_oauth2)]

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

DPSes = Annotated[AsyncSession, Depends(get_session)]

async def get_current_user(db: DPSes, token: DPToken):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    stmt = select(User).where(User.email == token_data.sub)
    res = await db.exec(stmt)
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user