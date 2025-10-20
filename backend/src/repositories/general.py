from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.repositories.athlete import AthleteRepository
from backend.src.repositories.base import BaseRepository
from backend.src.repositories.user import UserRepository


class Repository(BaseRepository):
    athletes: AthleteRepository
    users: UserRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.athletes = AthleteRepository(session=session)
        self.users = UserRepository(session=session)
