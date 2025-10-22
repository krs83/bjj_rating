from backend.src.exceptions.base import NotFoundException, ConflictException


class UserNotFoundException(NotFoundException):
    USERNOTFOUNDTEXT = "Пользователь с ID №{} не найден"

    def __init__(self, user_id: int):
        super().__init__(detail=self.USERNOTFOUNDTEXT.format(user_id))

class UserConflictException(ConflictException):
    USERCONFLICTTEXT = "Пользователь с e-mail {} уже существует"

    def __init__(self,  email: str):
        super().__init__(detail=self.USERCONFLICTTEXT.format(email))