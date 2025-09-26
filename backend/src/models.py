from datetime import date

from sqlmodel import Field, SQLModel, String, Date, Relationship, Column
from pydantic import ConfigDict

class AthleteTournamentLink(SQLModel, table=True):
    athlete_id: int | None = Field(default=None, foreign_key='athlete.id', primary_key=True)
    tournament_id: int | None = Field(default=None, foreign_key='tournament.id', primary_key=True)

class AthleteBase(SQLModel):
    fullname: str = Field(String(50),index=True, nullable=False)
    birth: date = Field(sa_column=Column(Date, index=True))
    city: str = Field(String(50))
    region: str = Field(String(50),index=True, nullable=False)
    points: int | None = Field(index=True, default=None, ge=0)

class Athlete(AthleteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    place: int | None = Field(default=None)

    tournaments: list["Tournament"] = Relationship(back_populates='athletes',
                                                      link_model=AthleteTournamentLink)

class AthleteResponse(AthleteBase):
    id: int
    place: int

    model_config = ConfigDict(from_attributes=True)

class AthleteAdd(AthleteBase):
    pass

class AthleteUpdate(SQLModel):
    fullname: str | None = None
    birth: date | None  = None
    city: str | None  = None
    region: str | None  = None
    points: int | None = None

class Tournament(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String(50),index=True, nullable=False)
    smoothcomp_id: int = Field(nullable=False)
    smoothcomp_date: date = Field(sa_column=Column(Date))

    athletes: list[Athlete] = Relationship(back_populates='tournaments',
                                             link_model=AthleteTournamentLink)

