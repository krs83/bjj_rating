from sqlmodel import select
from backend.src.models import Athlete, Tournament, AthleteResponse, AthleteAdd, AthleteUpdate
from backend.src.dependencies import DPSes
from backend.src.utility import find_existing_athlete, calculating_place
#TODO: пройтись mypy в конце


#Athlete crud
async def get_athletes(db: DPSes, offset: int, limit: int):
    stmt = select(Athlete).offset(offset).limit(limit)
    res = await db.exec(stmt)
    athletes = res.all()
    return athletes

async def get_athlete(db: DPSes, athlete_id: int):
    athlete = await db.get(Athlete, athlete_id)
    # TODO: Проверка на наличие id - if not athlete: Exception
    return athlete

async def create_athlete(db: DPSes, athlete_data: AthleteAdd):
    athlete = await find_existing_athlete(db, athlete_data)
    db.add(athlete)
    await db.commit() # TODO: оптимизировать запросы. Пока 2
    await db.refresh(athlete)
    await calculating_place(db)
    await db.commit()
    return athlete_data

async def part_update_athlete(db: DPSes, athlete_id:int, athlete_data: AthleteUpdate):
    db_athlete = await db.get(Athlete, athlete_id)
    # TODO: Проверка на наличие id - if not db_athlete: Exception
    athlete = athlete_data.model_dump(exclude_unset=True)
    db_athlete.sqlmodel_update(athlete)
    db.add(db_athlete)
    await db.commit()
    await calculating_place(db)
    await db.refresh(db_athlete)
    return AthleteResponse.model_validate(db_athlete)
