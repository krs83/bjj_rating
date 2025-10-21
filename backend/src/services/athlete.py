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
        """Получение всех спортсменов из БД согласно выборке"""
        self.logger.info(f"Получен список всех спортсменов из БД согласно выборке")

        return await self.repository.athletes.get_athletes(offset=offset, limit=limit)

    async def get_athlete(self, athlete_id: int) -> Athlete:
        """Получение конкретного спортсмена по ID"""

        athlete =  await self.repository.athletes.get_athlete_by_id(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.AthleteNotFoundText.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно получен")
        return athlete

    async def create_athlete(self, athlete_data: AthleteAdd) -> AthleteResponse:
        """Добавление записи в БД о новом спортсмене"""

        athlete = await self.find_existing_athlete(athlete_data)

        await self.repository.athletes.create_athlete(athlete)

        await self.repository.athletes.calculating_place()
        await self.session.refresh(athlete)
        self.logger.info(f"Добавлен новый спортсмен")

        return AthleteResponse.model_validate(athlete)

    async def part_update_athlete(self, athlete_id: int, athlete_data: AthleteUpdate) -> AthleteResponse:
        """Частичное или полное обновление данных о спортсмене по его ID"""

        athlete = athlete_data.model_dump(exclude_unset=True)

        db_athlete = await self.repository.athletes.update_athlete(
            athlete_id=athlete_id, athlete_data=athlete
        )
        if not db_athlete:
            self.logger.error(AthleteNotFoundException.AthleteNotFoundText.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        await self.repository.athletes.calculating_place()
        await self.session.refresh(db_athlete)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно обновлён")

        return AthleteResponse.model_validate(db_athlete)

    async def del_athlete(self, athlete_id: int) -> bool:
        """Удаление записи о спортсмене из БД по его ID"""

        athlete =  await self.repository.athletes.delete_athlete(athlete_id)
        if not athlete:
            self.logger.error(AthleteNotFoundException.AthleteNotFoundText.format(athlete_id))
            raise AthleteNotFoundException(athlete_id)
        self.logger.info(f"Спортсмен с ID №{athlete_id} успешно удалён")

        return athlete


    async def find_existing_athlete(self, athlete_data: AthleteAdd) -> Athlete:
        """Если будет совпадение по имени, ДР и региону, новый спортсмен не добавляется\n
       Только суммируются баллы\n
        В противном случае - добавляется новый спортсмен
        """

        athlete = await self.repository.athletes.get_athlete_by_conditions(athlete_data)

        if athlete:
            athlete.points += athlete_data.points
            self.logger.info(f"Баллы спортсмена обновлены - {athlete.points} ")

            return athlete
        else:
            new_athlete = Athlete.model_validate(athlete_data)
            self.logger.info(f"Добавлен новый спортсмен")

            return new_athlete





