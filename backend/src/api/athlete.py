from fastapi import APIRouter, Query

from backend.src.crud.athlete import get_athlete, get_athletes, create_athlete, part_update_athlete, delete_athlete
from backend.src.dependencies import DPSes
from backend.src.models.athlete import AthleteAdd, AthleteResponse, AthleteBase, AthleteUpdate

router = APIRouter(prefix='/athletes', tags=['Спортсмены'])

@router.get('', response_model=list[AthleteResponse])
async def get_all_athletes(db: DPSes, offset: int = 0, limit: int = Query(default=50, le=100)) -> AthleteBase:
    return await get_athletes(db, offset, limit)

@router.get('/{athlete_id}', response_model=AthleteResponse)
async def get_one_athlete(db: DPSes, athlete_id: int) -> AthleteBase:
    return await get_athlete(db, athlete_id)

@router.post('', response_model=AthleteResponse)
async def add_athlete(db: DPSes, athlete_data: AthleteAdd) -> AthleteBase:
    return await create_athlete(db, athlete_data)

@router.patch('/{athlete_id}', response_model=AthleteResponse)
async def update_athlete(db: DPSes, athlete_id: int, athlete_data: AthleteUpdate) -> AthleteBase:
    return await part_update_athlete(db, athlete_id, athlete_data)

@router.delete('/{athlete_id}')
async def del_athlete(db: DPSes, athlete_id: int):
    return await delete_athlete(db, athlete_id)