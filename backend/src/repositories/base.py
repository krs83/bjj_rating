from typing import Any, cast, TypeVar
from sqlalchemy import ColumnExpressionArgument
from sqlalchemy.orm import InstrumentedAttribute
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

T = TypeVar("T")
type ColumnClauseType[T] = type[T] | InstrumentedAttribute[T]


class BaseRepository:
    """Базовый репозиторий для работы с БД"""
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_one(
        self, model: ColumnClauseType[T], *conditions: ColumnExpressionArgument[Any]
    ) -> T | None:
        query = select(model).where(*conditions)
        result = await self.session.exec(query)
        return result.first()

    async def _get_pk(self, model: ColumnClauseType[T], pk: int) -> T | None:
        return await self.session.get(model, pk)

    async def _get_many(
        self,
        model: ColumnClauseType[T],
        offset: int = 0,
        limit: int = 100,
        order_by: Any | None = None,
    ) -> list[T]:
        query = select(model)
        if order_by is not None:
            query = query.order_by(order_by)
        query = query.offset(offset).limit(limit)

        result = await self.session.exec(query)
        return result.all()

    async def _update(
        self,
        model: ColumnClauseType[T],
        model_data: dict[str, Any],
        pk: int,
        extra: dict[str, Any] | None = None,
    ) -> T | None:
        obj = await self._get_pk(model, pk)
        if obj is not None:
            obj.sqlmodel_update(model_data, update=extra)
            self.session.add(obj)
            return obj
        return None

    async def _delete(
        self, model: ColumnClauseType[T], *conditions: ColumnExpressionArgument[Any]
    ) -> bool:
        result = await self.session.exec(delete(model).where(*conditions))
        return cast(bool, result.rowcount > 0)
