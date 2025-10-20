from sqladmin import ModelView

from backend.src.models import Tournament


class TournamentAdmin(ModelView, model=Tournament):
    column_list = "__all__"
