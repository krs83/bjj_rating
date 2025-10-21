from typing import Any

from backend.src.models.athlete import Athlete, AthleteAdd
from backend.src.repositories.base import BaseRepository


class AthleteRepository(BaseRepository):

    async def get_athletes(self,
                           offset: int,
                           limit: int,
                           order_by=Athlete.place.asc()) ->list[Athlete]:

        result = await self._get_many(
            model=Athlete, offset=offset, limit=limit, order_by=order_by
        )
        return result

    async def get_athlete_by_id(self, athlete_id: int) -> Athlete:
        return await self._get_pk(model=Athlete, pk=athlete_id)

    async def get_athlete_by_conditions(self, athlete_data: AthleteAdd) -> Athlete:
       return await self._get_one(
            Athlete,
            Athlete.fullname == athlete_data.fullname,
            Athlete.birth == athlete_data.birth,
            Athlete.region == athlete_data.region,
        )

    async def create_athlete(self, db_athlete: Athlete) -> Athlete:
        self.session.add(db_athlete)
        await self.session.commit()
        await self.session.refresh(db_athlete)
        return db_athlete

    async def update_athlete(
        self, athlete_id: int, athlete_data: dict[str, Any]
    ) -> Athlete | None:
        db_athlete = await self._update(Athlete, athlete_data, athlete_id)
        if db_athlete is not None:
            await self.session.commit()
            await self.session.refresh(db_athlete)
            return db_athlete
        return None

    async def delete_athlete(self, athlete_id: int) -> bool:
        result = await self._delete(Athlete, Athlete.id == athlete_id)
        await self.session.commit()
        return result

    async def calculating_place(self) -> None:
        athletes = await self.get_athletes(
            offset=0, limit=100, order_by=Athlete.points.desc()
        )

        for i, athlete in enumerate(athletes, start=1):
            athlete.place = i

        await self.session.commit()
