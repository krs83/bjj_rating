from sqlmodel import select, col
from backend.src.models import Athlete, Tournament
from backend.src.dependecies import DBSes

#Athlete crud
async def get_athletes(db: DBSes, offset: int = 0, limit: int = 50):
    stmt = select(Athlete).offset(offset).limit(limit)
    res = db.exec(stmt).all()
    return res

async def get_one_athlete(db: DBSes, athlete_id: int):
    stmt = select(Athlete).where(col(Athlete.id == athlete_id))
    res = db.exec(stmt).first()
    return res

