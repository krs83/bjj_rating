from pydantic import EmailStr
from sqlmodel import select
from backend.src.models.user import User, UserAdd
from backend.src.dependencies import DPSes

#TODO: пройтись mypy в конце

# User crud
async def get_users(db: DPSes, offset: int, limit: int):
    stmt = select(User).offset(offset).limit(limit)
    res = await db.exec(stmt)
    users = res.all()
    return users

async def get_user_by_id(db: DPSes, user_id: int):
    user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not user: Exception
    return user

async def get_user_by_email(db: DPSes, user_email: EmailStr) -> User:
    stmt = select(User).where(User.email == user_email )
    res = await db.exec(stmt)
    user = res.first()
    # TODO: Проверка на наличие id - if not user: Exception
    return user

async def delete_user(db: DPSes, user_id:int):
    user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not user_id: Exception
    await db.delete(user)
    await db.commit()
    return {'ok': True}