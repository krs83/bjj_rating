from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.crud.auth import login_access_token
from backend.src.dependencies import DPSes, CurrentUser
from backend.src.models.token import Token
from backend.src.models.user import UserLogin, UserResponse

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


#TODO: добавь во все ручки HTTPException


@router.post('/login/access_token', response_model=Token)
async def login_user(db: DPSes,
                     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     ) -> Token:
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return await login_access_token(db, user_data)

@router.get('/me', response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


# @router.post('/logout')
# async def logout(response: Response):
#     pass
