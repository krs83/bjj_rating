from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from backend.app.database_settings import db_settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(db_settings.DB_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass