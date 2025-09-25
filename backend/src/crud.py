from sqlmodel import select
from backend.src.models import Athlete, Tournament, AthleteResponse, AthleteAdd
from backend.src.dependencies import DPSes
from backend.src.utility import find_existing_athlete, calculating_place


#Athlete crud
async def get_athletes(db: DPSes, offset: int, limit: int):
    stmt = select(Athlete).offset(offset).limit(limit)
    res = await db.exec(stmt)
    athletes = res.all()
    athletes = [AthleteResponse.model_validate(athlete) for athlete in athletes]
    return athletes

async def get_athlete(db: DPSes, athlete_id: int):
    stmt = select(Athlete).where(Athlete.id == athlete_id)
    res = await db.exec(stmt)
    athlete = res.one()
    return athlete

async def create_athlete(db: DPSes, athlete_data: AthleteAdd):
    athlete = await find_existing_athlete(db, athlete_data)
    await calculating_place(db)
    db.add(athlete)
    await db.commit()
    return athlete_data
