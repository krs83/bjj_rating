from datetime import date

from sqlalchemy import String,Date
from sqlmodel import Field, SQLModel


class Tournaments(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(String(50), nullable=False)
    smoothcomp_id: int = Field(nullable=False)
    smoothcomp_date: date = Date


