from backend.src.exceptions.base import NotFoundException



class AthleteNotFoundException(NotFoundException):
    AthleteNotFoundText = "Спортсмен с ID №{} не найден"

    def __init__(self, athlete_id: int):
        super().__init__(detail=self.AthleteNotFoundText.format(athlete_id))