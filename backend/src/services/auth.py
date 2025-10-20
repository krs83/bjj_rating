from pydantic import EmailStr

from backend.src.models.token import Token
from backend.src.models.user import UserLogin
from backend.src.security import verify_password, create_access_token
from backend.src.services.base import BaseService


class AuthService(BaseService):
    async def authenticate_user(self, user_email: EmailStr, password: str):
        user = await self.repository.users.get_user_by_email(user_email)
        if not user:
            return False  # TODO: добавь NoSuchUserException
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def login_access_token(self, user_data: UserLogin):
        user = await self.authenticate_user(user_data.email, user_data.password)
        if not user:
            return False  # TODO: добавь отработку Exception
        data = {"sub": user.email, "is_admin": user.is_admin}
        access_token = create_access_token(data=data)
        return Token(access_token=access_token)

    # async def log_out(self, response, request):
    #     if "access_token" in request.cookies:
    #         response.delete_cookie("access_token")
    #         return {"Status": "You are logged out! See you later!"}
    #     else:
    #         return {"error": "You are already logged out!"}
