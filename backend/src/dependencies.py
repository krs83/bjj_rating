from fastapi import Depends
from typing import Annotated

from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.database import engine


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

DPSes = Annotated[AsyncSession, Depends(get_session)]