from backend.src.models.user import (
    UserCreate,
    User,
    UserResponse,
    UserUpdate,
    UserLogin,
)
from backend.src.security import hash_password
from backend.src.services.base import BaseService


class UserService(BaseService):
    async def get_users(self, offset: int, limit: int) -> list[User]:
        return await self.repository.users.get_users(offset=offset, limit=limit)

    async def get_user(self, user_id: int) -> User:
        return await self.repository.users.get_user_by_id(user_id)

    async def create_user(
        self,
        user_data: UserCreate | UserLogin,
    ) -> UserResponse:
        hashed_password = hash_password(user_data.password)
        extra_data = {"hashed_password": hashed_password}

        db_user = User.model_validate(user_data, update=extra_data)

        await self.repository.users.create_user(db_user)
        return UserResponse.model_validate(db_user)

    async def part_update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ):
        # TODO: Проверка на наличие id - if not db_user: Exception
        user = user_data.model_dump(exclude_unset=True)
        extra_data = {}
        if "password" in user:
            password = user["password"]
            hashed_password = hash_password(password)
            extra_data["hashed_password"] = hashed_password
        db_user = await self.repository.users.update_user(
            user_id=user_id, user_data=user, extra_data=extra_data
        )
        return UserResponse.model_validate(db_user)

    async def del_user(self, user_id: int):
        return await self.repository.users.delete_user(user_id)
