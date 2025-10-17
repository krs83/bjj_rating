from typing import Any

from fastapi import APIRouter, Query
from fastapi.params import Depends

from backend.src.crud.user import create_user, get_users, get_user_by_id, part_update_user, delete_user
from backend.src.dependencies import DPSes, CurrentUser, get_current_admin
from backend.src.models.user import UserCreate, UserResponse, UserUpdate, UserLogin

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/', dependencies=[Depends(get_current_admin)], response_model=UserResponse)
async def user_create(db: DPSes, user_data: UserCreate) -> Any:
    """
   Создание пользователя админом
    """
    return await create_user(db, user_data)


@router.post('/signup', response_model=UserResponse)
async def register_user(db: DPSes, user_data: UserLogin) -> Any:
    """
   Регистрация пользователя без аутентификации
    """
    _user_create = UserCreate.model_validate(user_data)
    return await create_user(db, _user_create)


@router.get('', response_model=list[UserResponse])
async def get_all_users(db: DPSes,
                        current_user: CurrentUser,
                        offset: int = 0,
                        limit: int = Query(default=50, le=100)) -> Any:
    print(f'{current_user=}')
    return await get_users(db, offset, limit)


@router.get('/{user_id}', response_model=UserResponse)
async def get_one_user(db: DPSes, user_id: int) -> Any:
    return await get_user_by_id(db, user_id)


@router.patch('/{user_id}', response_model=UserResponse)
async def update_user(db: DPSes, user_id: int, user_data: UserUpdate) -> Any:
    return await part_update_user(db, user_id, user_data)


@router.delete('/{user_id}')
async def del_user(db: DPSes, user_id: int):
    return await delete_user(db, user_id)