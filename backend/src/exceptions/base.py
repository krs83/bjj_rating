from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundException(BaseAppException):
    def __init__(self, detail: str = "Не найдено"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


