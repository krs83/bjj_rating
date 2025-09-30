from typing import Annotated

from fastapi import APIRouter, Response, Request
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.crud.auth import login_access_token, part_update_user, log_out
from backend.src.crud.auth import create_user
from backend.src.dependencies import DPSes
from backend.src.models.token import Token
from backend.src.models.user import UserResponse, UserAdd, UserBase, UserUpdate, UserLogin

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])
#TODO: добавь во все ручки HTTPException

@router.post('/sign', response_model=UserResponse)
async def register_user(db: DPSes, user_data: UserAdd) -> UserBase:
    return await create_user(db, user_data)

@router.post('/login/access_token', response_model=Token)
async def login_user(db: DPSes, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     response: Response) -> Token:
    user_data = UserLogin(email=form_data.username, password=form_data.password)
    return await login_access_token(db, user_data, response)

@router.patch('/user_id', response_model=UserResponse)
async def update_user(db: DPSes, user_id: int, user_data: UserUpdate) -> UserBase:
    return await part_update_user(db, user_id, user_data)

@router.post('/logout')
async def logout(response: Response, request: Request):
    return await log_out(response, request)