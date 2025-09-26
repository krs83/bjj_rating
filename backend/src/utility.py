from sqlmodel import select
from passlib.hash import pbkdf2_sha256

from backend.src.dependencies import DPSes
from backend.src.models.athlete import AthleteAdd, Athlete


async def find_existing_athlete(db: DPSes, athlete_data: AthleteAdd):
    stmt = select(Athlete).where(
        Athlete.fullname == athlete_data.fullname,
                    Athlete.birth == athlete_data.birth,
                    Athlete.region == athlete_data.region
    )
    result = await db.exec(stmt)
    athlete = result.first()

    if athlete:
        athlete.points += athlete_data.points
        return athlete
    else:
        new_athlete = Athlete.model_validate(athlete_data)
        return new_athlete

async def calculating_place(db: DPSes):
    stmt = select(Athlete).order_by(Athlete.points.desc())
    result = await db.exec(stmt)
    athletes = result.all()

    for i,athlete in enumerate(athletes, start=1):
        athlete.place = i

    await db.commit()

def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


