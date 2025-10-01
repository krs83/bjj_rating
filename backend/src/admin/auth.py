from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from backend.src.admin.dependency import session_maker_admin

from backend.src.models.user import User
from backend.src.security import verify_password

async def authenticate_user(db: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if user:
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
            user = await authenticate_user(db, email, password)

            if user:
                request.session.update({
                    'authenticated': True,
                    'email': email,
                    'role': user.role
                })
                return True
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        email = request.session.get("email")

        if not email:
            return False
        return True

