from backend.src.exceptions.athlete import AthleteNotFoundException
from backend.src.models.athlete import (
    AthleteAdd,
    AthleteResponse,
    Athlete,
    AthleteUpdate,
)
from backend.src.services.base import BaseService


class AthleteService(BaseService):
    async def get_athletes(self, offset: int, limit: int) -> list[Athlete]:
        return await self.repository.athletes.get_athletes(offset=offset, limit=limit)

    async def get_athlete(self, athlete_id: int) -> Athlete:
        athlete =  await self.repository.athletes.get_athlete_by_id(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.AthleteNotFoundText.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        return athlete

    async def create_athlete(self, athlete_data: AthleteAdd) -> AthleteResponse:
        athlete = await self.find_existing_athlete(athlete_data)

        # TODO: оптимизировать запросы. Пока 2
        # TODO: обработать ошибку если введены не все поля
        await self.repository.athletes.create_athlete(athlete)

        await self.repository.athletes.calculating_place()
        await self.session.refresh(athlete)

        return AthleteResponse.model_validate(athlete)

    async def part_update_athlete(self, athlete_id: int, athlete_data: AthleteUpdate):
        # TODO: Проверка на наличие id - if not athlete: Exception
        athlete = athlete_data.model_dump(exclude_unset=True)

        db_athlete = await self.repository.athletes.update_athlete(
            athlete_id=athlete_id, athlete_data=athlete
        )
        await self.repository.athletes.calculating_place()
        await self.session.refresh(db_athlete)

        return AthleteResponse.model_validate(db_athlete)

    async def del_athlete(self, athlete_id: int):
        return await self.repository.athletes.delete_athlete(athlete_id)

    async def find_existing_athlete(self, athlete_data: AthleteAdd):
        athlete = await self.repository.athletes.get_athlete_by_conditions(athlete_data)

        if athlete:
            athlete.points += athlete_data.points
            return athlete
        else:
            new_athlete = Athlete.model_validate(athlete_data)
            return new_athlete





