from backend.src.exceptions.base import NotFoundException, ConflictException


class AthleteTournamentLinkIntegrityException(ConflictException):
    ATHLETETOURNAMENTLINKNOTFOUNDTEXT = "Данные неверные"

    def __init__(self):
        super().__init__(detail=self.ATHLETETOURNAMENTLINKNOTFOUNDTEXT)