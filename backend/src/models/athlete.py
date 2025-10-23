from datetime import date

from sqlmodel import Field, SQLModel, String, Date, Relationship, Column

from backend.src.models import AthleteTournamentLink


class AthleteBase(SQLModel):
    fullname: str = Field(String(50), index=True, nullable=False)
    birth: date = Field(sa_column=Column(Date, index=True))
    city: str = Field(String(50))
    region: str = Field(String(50), index=True, nullable=False)
    points: int = Field(index=True, default=0, ge=0)


class Athlete(AthleteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    place: int | None = Field(default=None)

    tournaments: list["Tournament"] = Relationship(
        back_populates="athletes", link_model=AthleteTournamentLink
    )


class AthleteResponse(AthleteBase):
    id: int
    place: int


class AthleteAdd(AthleteBase):
    pass


class AthleteUpdate(SQLModel):
    fullname: str | None = None
    birth: date | None = None
    city: str | None = None
    region: str | None = None
    points: int | None = None
