from backend.src.exceptions.base import ConflictException


class AthleteTournamentLinkIntegrityException(ConflictException):
    ATHLETETOURNAMENTLINKEXISTSTEXT = "ID турнира(ов) уже существует в БД. Пожалуйста, проверьте!"

    def __init__(self):
        super().__init__(detail=self.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)