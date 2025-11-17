from typing import List

from fastapi import APIRouter, Query, Depends

from backend.src.dependencies import athlete_serviceDP, get_current_admin, athlete_tournament_link_serviceDP
from backend.src.models.athlete import (
    AthleteAdd,
    AthleteResponse,
    AthleteBase,
    AthleteUpdate,
    Athlete,
)
from backend.src.models.athlete_tournament import AthleteTournamentLinkResponse, AthleteTournamentLinkBase, \
    AthleteTournamentLinkAdd

router = APIRouter(prefix="/athlete_tournament_link", tags=["Спортсмен-турнир-связь"])


# @router.get("",
#             response_model=list[AthleteResponse],
#             description="Получение списка всех спортсменов",
#             summary="Get athletes list")
# async def get_all_athletes(
#     athlete_service: athlete_serviceDP,
#     offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
#     limit: int = Query(default=50, le=100, description="Лимит записей на страницу"),
# ) -> list[Athlete]:
#     return await athlete_service.get_athletes(offset, limit)
#
#
# @router.get("/{athlete_id}",
#             response_model=AthleteResponse,
#             description="Получение спортсмена по ID",
#             summary="Get athlete by ID")
# async def get_one_athlete(
#     athlete_service: athlete_serviceDP, athlete_id: int
# ) -> AthleteBase:
#     return await athlete_service.get_athlete(athlete_id)


@router.post("",
             dependencies=[Depends(get_current_admin)],
             response_model=AthleteTournamentLinkResponse,
             description="Добавление связи спортсмен-турнир в БД",
             summary="Add athlete tournament link to DB")
async def add_athlete_tournament_link(
        athlete_tournament_link_service: athlete_tournament_link_serviceDP,
        athlete_tournament_link_data: AthleteTournamentLinkAdd
) -> AthleteTournamentLinkBase:
    return await athlete_tournament_link_service.create_athlete_tournament_link(athlete_tournament_link_data)


# @router.post("/bulk",
#              dependencies=[Depends(get_current_admin)],
#              response_model=List[AthleteResponse],
#              description="Добавление списка записей о спортсменах в БД",
#              summary="Add athletes list to DB")
# async def add_few_athletes(
#         athlete_service: athlete_serviceDP, athlete_data: List[AthleteAdd]
# ) -> List[AthleteResponse]:
#     return await athlete_service.create_few_athletes(athlete_data)
#
#
# @router.patch("/{athlete_id}",
#               dependencies=[Depends(get_current_admin)],
#               response_model=AthleteResponse,
#               description="Обновление данных о спортсмене по ID",
#               summary="Update athlete by ID")
# async def update_athlete(
#     athlete_service: athlete_serviceDP, athlete_id: int, athlete_data: AthleteUpdate
# ) -> AthleteBase:
#     return await athlete_service.part_update_athlete(athlete_id, athlete_data)
#
#
@router.delete("/{athlete_id}/{tournament_id}",
               dependencies=[Depends(get_current_admin)],
               description="Удаление связи о спортсмене-турнире из БД по ID",
               summary="Delete athlete_tournament_link by ID")
async def del_athlete_tournament_link(athlete_tournament_link_service: athlete_tournament_link_serviceDP,
                      athlete_id: int,
                      tournament_id: int) -> bool:
    return await athlete_tournament_link_service.del_athlete_tournament_link(athlete_id, tournament_id)
