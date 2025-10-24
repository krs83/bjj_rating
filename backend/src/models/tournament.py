from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, String, Date, Relationship, Column

from backend.src.models import AthleteTournamentLink

if TYPE_CHECKING:
    from backend.src.models import Athlete

class Tournament(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String(50), index=True, nullable=False)
    smoothcomp_id: int = Field(nullable=False)
    smoothcomp_date: date = Field(sa_column=Column(Date))

    athletes: list["Athlete"] = Relationship(
        back_populates="tournaments", link_model=AthleteTournamentLink
    )
