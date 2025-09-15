from datetime import date

from sqlalchemy import String,Date
from sqlmodel import Field, SQLModel


class Athlete(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(String(50), nullable=False)
    surname: str = Field(String(50), nullable=False)
    birth: date = Date
    points: int = Field(default=0, ge=0)


