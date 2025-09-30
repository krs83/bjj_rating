from fastapi import Depends
from typing import Annotated
import jwt

from fastapi.security import OAuth2PasswordBearer
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
    print(f'{token=}')
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    token_data = TokenData(**payload)
    stmt = select(User).where(User.email == token_data.sub )
    res = await db.exec(stmt)
    user = res.first()
    print(f'{user=}')
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]