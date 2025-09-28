from sqlmodel import Field, SQLModel


class AthleteTournamentLink(SQLModel, table=True):
    athlete_id: int | None = Field(default=None, foreign_key='athlete.id', primary_key=True)
    tournament_id: int | None = Field(default=None, foreign_key='tournament.id', primary_key=True)
