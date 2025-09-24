from fastapi import APIRouter

from backend.src.crud import get_athlete, get_athletes
from backend.src.dependencies import DBSes

r_athletes = APIRouter(prefix='/athletes', tags=['Спортсмены'])

# Athletes endpoints
@r_athletes.get('')
async def get_all_athletes(db: DBSes, offset: int = 0, limit: int = 50):
    return await get_athletes(db, offset, limit)

@r_athletes.get('/athlete_id')
async def get_one_athlete(db: DBSes, athlete_id: int):
    return await get_athlete(db, athlete_id)