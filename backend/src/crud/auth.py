
from pydantic import EmailStr

from backend.src.crud.user import get_user_by_email
from backend.src.dependencies import DPSes
from backend.src.models.user import UserAdd, User, UserResponse, UserUpdate, UserLogin
from backend.src.models.token import Token
from backend.src.security import hash_password, verify_password, create_access_token

#TODO: перевести в ООП и остальное тоже
#TODO: поставь в директориях init чтобы импортировать не функции а файл.функция (только файл)

token_type = 'bearer'


async def create_user(db: DPSes, user_data: UserAdd):
    hashed_password = hash_password(user_data.password)
    extra_data = {'hashed_password': hashed_password}
    db_user = User.model_validate(user_data, update=extra_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)


async def authenticate_user(db: DPSes, user_email: EmailStr, password: str):
    user = await get_user_by_email(db, user_email)
    if not user:
        return False  #TODO: добавь NoSuchUserException
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def login_access_token(db: DPSes, user_data: UserLogin, response):
    user = await authenticate_user(db, user_data.email, user_data.password)
    if not user:
        return False  #TODO: добавь отработку Exception
    access_token = create_access_token(data={'sub': user.email})
    response.set_cookie("access_token", access_token)
    return Token(access_token=access_token, token_type=token_type)


async def part_update_user(db: DPSes, user_id: int, user_data: UserUpdate):
    db_user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not db_user: Exception
    user = user_data.model_dump(exclude_unset=True)
    extra_data = {}
    if 'password' in user:
        password = user['password']
        hashed_password = hash_password(password)
        extra_data['hashed_password'] = hashed_password
    db_user.sqlmodel_update(user, update=extra_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)


async def log_out(response, request):
    if "access_token" in request.cookies:
        response.delete_cookie("access_token")
        return {"Status": "You are logged out! See you later!"}
    else:
        return {"error": "You are already logged out!"}
