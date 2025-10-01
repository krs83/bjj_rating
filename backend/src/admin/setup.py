from sqladmin import Admin

from backend.src.database import engine
from backend.src.admin.user import UserAdmin
from backend.src.admin.athlete import AthleteAdmin
from backend.src.admin.tournament import TournamentAdmin
from backend.src.admin.athlete_tournament import AthleteTournamentLinkAdmin


def setup_admin(app):
    admin = Admin(app=app,
                  engine=engine,
                  title='BJJ RATING ADMINISTRATOR')

    admin.add_view(UserAdmin)
    admin.add_view(AthleteAdmin)
    admin.add_view(TournamentAdmin)
    admin.add_view(AthleteTournamentLinkAdmin)

