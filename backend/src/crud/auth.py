
from pydantic import EmailStr

from backend.src.crud.user import get_user_by_email
from backend.src.dependencies import DPSes
from backend.src.models.token import Token
from backend.src import security
from backend.src.models.user import UserLogin, User
from backend.src.security import verify_password

#TODO: перевести в ООП и остальное тоже
#TODO: поставь в директориях init чтобы импортировать не функции а файл.функция (только файл)


async def authenticate_user(db: DPSes, user_email: EmailStr, password: str):
    user = await get_user_by_email(db, user_email)
    if not user:
        return False  #TODO: добавь NoSuchUserException
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def login_access_token(db: DPSes, user_data: UserLogin):
    user = await authenticate_user(db, user_data.email, user_data.password)
    if not user:
        return False  #TODO: добавь отработку Exception
    data = {'sub': user.email,
            'is_admin': user.is_admin}
    access_token = security.create_access_token(data=data)
    return Token(access_token=access_token)


# async def log_out(response, request):
#     if "access_token" in request.cookies:
#         response.delete_cookie("access_token")
#         return {"Status": "You are logged out! See you later!"}
#     else:
#         return {"error": "You are already logged out!"}
