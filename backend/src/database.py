from sqlalchemy.ext.asyncio import create_async_engine
from backend.src.database_settings import settings

engine = create_async_engine(settings.DB_URL, echo=True)

