from datetime import date

from sqlmodel import Field, SQLModel, String, Date, Relationship, Column
from pydantic import ConfigDict

class AthleteTournamentLink(SQLModel, table=True):
    athlete_id: int | None = Field(default=None, foreign_key='athlete.id', primary_key=True)
    tournament_id: int | None = Field(default=None, foreign_key='tournament.id', primary_key=True)


class Athlete(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    place: int = Field(nullable=False)
    fullname: str = Field(String(50),index=True, nullable=False)
    birth: date = Field(sa_column=Column(Date))
    city: str = Field(String(50),index=True)
    region: str = Field(String(50),index=True, nullable=False)
    points: int = Field(default=0, ge=0)

    tournaments: list["Tournament"] = Relationship(back_populates='athletes',
                                                   link_model=AthleteTournamentLink)

class AthleteResponse(SQLModel):
    id: int
    fullname: str
    place: int
    fullname: str
    birth: date
    city: str
    region: str
    points: int

    model_config = ConfigDict(from_attributes=True)

class AthleteAdd(SQLModel):
    fullname: str = Field(String(50),index=True, nullable=False)
    birth: date = Field(sa_column=Column(Date))
    city: str = Field(String(50),index=True)
    region: str = Field(String(50),index=True, nullable=False)
    points: int

class Tournament(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String(50),index=True, nullable=False)
    smoothcomp_id: int = Field(nullable=False)
    smoothcomp_date: date = Field(sa_column=Column(Date))

    athletes: list[Athlete] = Relationship(back_populates='tournaments',
                                             link_model=AthleteTournamentLink)

