from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from jwt.exceptions import ExpiredSignatureError

from backend.src.admin.dependency import session_maker_admin

from backend.src.models.user import User
from backend.src.security import verify_password, create_access_token


async def authenticate_admin(db: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    print(f'{user=}')


    if user.is_admin:
        valid_password = verify_password(password, user.hashed_password)
        if valid_password:
            return user
        return None
    return None

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with session_maker_admin() as db:
            user = await authenticate_admin(db, email, password)

            if user:
                token = create_access_token({'sub': user.email})
                print(f'{token=}')

                request.session.update({'token': token})
                return True
            return False


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        try:
           request.session.get("token")

        except ExpiredSignatureError:
            await self.logout(request)
            return False
        return True


