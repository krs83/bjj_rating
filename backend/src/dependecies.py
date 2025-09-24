from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Session

from backend.src.database import engine


async def get_session():
    with Session(engine) as session:
        yield session

DBSes = Annotated[Session, Depends(get_session)]