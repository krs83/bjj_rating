from fastapi import APIRouter, Query

from backend.src.crud.user import get_user_by_id, get_users, delete_user
from backend.src.dependencies import DPSes, CurrentUser
from backend.src.models.user import  UserResponse, UserBase

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get('', response_model=list[UserResponse])
async def get_all_users(db: DPSes,
                        _: CurrentUser,
                        offset: int = 0,
                        limit: int = Query(default=50, le=100)) -> UserBase:
    return await get_users(db, offset, limit)

@router.get('/user_id', response_model=UserResponse)
async def get_one_user(db: DPSes, user_id: int) -> UserBase:
    return await get_user_by_id(db, user_id)

@router.delete('/user_id')
async def del_user(db: DPSes, user_id: int):
    return await delete_user(db, user_id)