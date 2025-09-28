from fastapi import APIRouter, Query

from backend.src.crud.user import get_user, get_users, create_user, part_update_user, delete_user
from backend.src.dependencies import DPSes
from backend.src.models.user import UserAdd, UserResponse, UserBase, UserUpdate

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get('', response_model=list[UserResponse])
async def get_all_users(db: DPSes, offset: int = 0, limit: int = Query(default=50, le=100)) -> UserBase:
    return await get_users(db, offset, limit)

@router.get('/user_id', response_model=UserResponse)
async def get_one_user(db: DPSes, user_id: int) -> UserBase:
    return await get_user(db, user_id)

@router.post('', response_model=UserResponse)
async def add_user(db: DPSes, user_data: UserAdd) -> UserBase:
    return await create_user(db, user_data)

@router.patch('/user_id', response_model=UserResponse)
async def update_user(db: DPSes, user_id: int, user_data: UserUpdate) -> UserBase:
    return await part_update_user(db, user_id, user_data)

@router.delete('/user_id')
async def del_user(db: DPSes, user_id: int):
    return await delete_user(db, user_id)