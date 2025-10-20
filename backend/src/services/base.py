import abc
import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.repositories.general import Repository


class BaseService(abc.ABC):
    repository: Repository
    session: AsyncSession

    def __init__(self, repository: Repository) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.repository = repository
        self.session = self.repository.session
