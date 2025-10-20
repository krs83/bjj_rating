from typing import Any

from fastapi import APIRouter, Query
from fastapi.params import Depends

from backend.src.dependencies import CurrentUser, get_current_admin, user_serviceDP
from backend.src.models.user import UserCreate, UserResponse, UserUpdate, UserLogin

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post(
    "/", dependencies=[Depends(get_current_admin)], response_model=UserResponse
)
async def user_create(user_service: user_serviceDP, user_data: UserCreate) -> Any:
    """
    Создание пользователя админом
    """
    return await user_service.create_user(user_data)


@router.post("/signup", response_model=UserResponse)
async def register_user(user_service: user_serviceDP, user_data: UserLogin) -> Any:
    """
    Регистрация пользователя без аутентификации
    """
    _user_create = UserCreate.model_validate(user_data)
    return await user_service.create_user(user_data)


@router.get("", response_model=list[UserResponse])
async def get_all_users(
    current_user: CurrentUser,
    user_service: user_serviceDP,
    offset: int = 0,
    limit: int = Query(default=50, le=100),
) -> Any:
    return await user_service.get_users(offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_one_user(user_service: user_serviceDP, user_id: int) -> Any:
    return await user_service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_service: user_serviceDP, user_id: int, user_data: UserUpdate
) -> Any:
    return await user_service.part_update_user(user_id, user_data)


@router.delete("/{user_id}")
async def del_user(user_service: user_serviceDP, user_id: int):
    return await user_service.del_user(user_id)
