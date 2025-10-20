from fastapi import APIRouter, Query

from backend.src.dependencies import athlete_serviceDP
from backend.src.models.athlete import (
    AthleteAdd,
    AthleteResponse,
    AthleteBase,
    AthleteUpdate,
    Athlete,
)

router = APIRouter(prefix="/athletes", tags=["Спортсмены"])


@router.get("", response_model=list[AthleteResponse])
async def get_all_athletes(
    athlete_service: athlete_serviceDP,
    offset: int = 0,
    limit: int = Query(default=50, le=100),
) -> list[Athlete]:
    return await athlete_service.get_athletes(offset, limit)


@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_one_athlete(
    athlete_service: athlete_serviceDP, athlete_id: int
) -> AthleteBase:
    return await athlete_service.get_athlete(athlete_id)


@router.post("", response_model=AthleteResponse)
async def add_athlete(
    athlete_service: athlete_serviceDP, athlete_data: AthleteAdd
) -> AthleteBase:
    return await athlete_service.create_athlete(athlete_data)


@router.patch("/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(
    athlete_service: athlete_serviceDP, athlete_id: int, athlete_data: AthleteUpdate
) -> AthleteBase:
    return await athlete_service.part_update_athlete(athlete_id, athlete_data)


@router.delete("/{athlete_id}")
async def del_athlete(athlete_service: athlete_serviceDP, athlete_id: int):
    return await athlete_service.del_athlete(athlete_id)
