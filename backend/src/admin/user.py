from sqladmin import ModelView
from backend.src.models import User


class UserAdmin(ModelView, model=User):
    column_list = "__all__"
