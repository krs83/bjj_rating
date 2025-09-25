from sqlmodel import select
from backend.src.models import Athlete, Tournament, AthleteResponse, AthleteAdd
from backend.src.dependencies import DPSes
from backend.src.utility import find_existing_athlete, calculating_place


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

# async def part_update_athlete(db: DPSes, athlete_id:int, athlete_data: AthleteAdd, unset=True):
#     stmt = select(Athlete).where(Athlete.id == athlete_id)
#     await db.exec(stmt)
#     db.add(athlete_data.model_dump(exclude_unset=unset))
#     await db.commit()
#     return athlete_data
#
# async def full_update_athlete(db: DPSes,  athlete_id:int, athlete_data: AthleteAdd, unset=False):
#     db.add(athlete_data.model_dump(exclude_unset=unset))
#     await db.commit()
#     return athlete_data
