from fastapi import APIRouter, Query

from backend.src.crud import get_athlete, get_athletes, create_athlete, part_update_athlete
from backend.src.dependencies import DPSes
from backend.src.models import AthleteAdd, AthleteResponse, AthleteBase, AthleteUpdate

r_athletes = APIRouter(prefix='/athletes', tags=['Спортсмены'])

# Athletes endpoints
@r_athletes.get('', response_model=list[AthleteResponse])
async def get_all_athletes(db: DPSes, offset: int = 0, limit: int = Query(default=50, le=100)) -> AthleteBase:
    return await get_athletes(db, offset, limit)

@r_athletes.get('/athlete_id', response_model=AthleteResponse)
async def get_one_athlete(db: DPSes, athlete_id: int) -> AthleteBase:
    return await get_athlete(db, athlete_id)

@r_athletes.post('', response_model=AthleteResponse)
async def add_athlete(db: DPSes, athlete_data: AthleteAdd) -> AthleteBase:
    return await create_athlete(db, athlete_data)

@r_athletes.patch('/athlete_id', response_model=AthleteResponse)
async def update_athlete(db: DPSes, athlete_id: int, athlete_data: AthleteUpdate) -> AthleteBase:
    return await part_update_athlete(db, athlete_id, athlete_data)