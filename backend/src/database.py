from sqlalchemy.ext.asyncio import create_async_engine
from backend.src.database_settings import db_settings

engine = create_async_engine(db_settings.DB_URL, echo=True)

