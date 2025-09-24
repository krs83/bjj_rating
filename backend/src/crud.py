from sqlmodel import select, col
from backend.src.models import Athlete, Tournament, AthleteResponse
from backend.src.dependencies import DBSes


#Athlete crud
async def get_athletes(db: DBSes, offset: int, limit: int):
    stmt = select(Athlete).offset(offset).limit(limit)
    res = await db.exec(stmt)
    athletes = res.all()
    athletes = [AthleteResponse.model_validate(athlete) for athlete in athletes]
    return athletes

async def get_athlete(db: DBSes, athlete_id: int):
    stmt = select(Athlete).where(Athlete.id == athlete_id)
    res = await db.exec(stmt)
    athlete = res.one()
    return athlete
