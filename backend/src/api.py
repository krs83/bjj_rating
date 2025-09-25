from fastapi import APIRouter

from backend.src.crud import get_athlete, get_athletes, create_athlete
from backend.src.dependencies import DPSes
from backend.src.models import AthleteAdd

r_athletes = APIRouter(prefix='/athletes', tags=['Спортсмены'])

# Athletes endpoints
@r_athletes.get('')
async def get_all_athletes(db: DPSes, offset: int = 0, limit: int = 50):
    return await get_athletes(db, offset, limit)

@r_athletes.get('/athlete_id')
async def get_one_athlete(db: DPSes, athlete_id: int):
    return await get_athlete(db, athlete_id)

@r_athletes.post('')
async def add_athlete(db: DPSes, athlete_data: AthleteAdd):
    return await create_athlete(db, athlete_data)