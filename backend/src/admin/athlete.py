from sqladmin import ModelView

from backend.src.models import Athlete


class AthleteAdmin(ModelView, model=Athlete):
    column_list = '__all__'