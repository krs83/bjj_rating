from fastapi import APIRouter, Response

from backend.src.crud.auth import log_in_user, part_update_user
from backend.src.crud.auth import create_user
from backend.src.dependencies import DPSes
from backend.src.models.token import Token
from backend.src.models.user import UserResponse, UserAdd, UserBase, UserUpdate

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])
#TODO: добавь во все ручки HTTPException

@router.post('/sign', response_model=UserResponse)
async def register_user(db: DPSes, user_data: UserAdd) -> UserBase:
    return await create_user(db, user_data)

@router.post('/login', response_model=Token)
async def login_user(db: DPSes, user_data: UserAdd, response: Response) -> Token:
    return await log_in_user(db, user_data, response)

@router.patch('/user_id', response_model=UserResponse)
async def update_user(db: DPSes, user_id: int, user_data: UserUpdate) -> UserBase:
    return await part_update_user(db, user_id, user_data)