from fastapi import APIRouter, Query, Depends

from backend.src.dependencies import athlete_serviceDP, get_current_admin
from backend.src.models.athlete import (
    AthleteAdd,
    AthleteResponse,
    AthleteBase,
    AthleteUpdate,
    Athlete,
)

router = APIRouter(prefix="/athletes", tags=["Спортсмены"])


@router.get("",
            response_model=list[AthleteResponse],
            description="Получение списка всех спортсменов",
            summary="Get athletes list")
async def get_all_athletes(
    athlete_service: athlete_serviceDP,
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(default=50, le=100, description="Лимит записей на страницу"),
) -> list[Athlete]:
    return await athlete_service.get_athletes(offset, limit)


@router.get("/{athlete_id}",
            response_model=AthleteResponse,
            description="Получение спортсмена по ID",
            summary="Get athlete by ID")
async def get_one_athlete(
    athlete_service: athlete_serviceDP, athlete_id: int
) -> AthleteBase:
    return await athlete_service.get_athlete(athlete_id)


@router.post("",
             dependencies=[Depends(get_current_admin)],
             response_model=AthleteResponse,
             description="Добавление записи о спортсмене в БД",
             summary="Add athlete to DB")
async def add_athlete(
    athlete_service: athlete_serviceDP, athlete_data: AthleteAdd
) -> AthleteBase:
    return await athlete_service.create_athlete(athlete_data)


@router.patch("/{athlete_id}",
              dependencies=[Depends(get_current_admin)],
              response_model=AthleteResponse,
              description="Обновление данных о спортсмене по ID",
              summary="Update athlete by ID")
async def update_athlete(
    athlete_service: athlete_serviceDP, athlete_id: int, athlete_data: AthleteUpdate
) -> AthleteBase:
    return await athlete_service.part_update_athlete(athlete_id, athlete_data)


@router.delete("/{athlete_id}",
               dependencies=[Depends(get_current_admin)],
               description="Удаление записи о спортсмене из БД по ID",
               summary="Delete athlete by ID")
async def del_athlete(athlete_service: athlete_serviceDP, athlete_id: int) -> bool:
    return await athlete_service.del_athlete(athlete_id)
