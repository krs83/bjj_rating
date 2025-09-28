from sqlmodel import select
from backend.src.models.user import  User, UserAdd, UserResponse, UserUpdate
from backend.src.dependencies import DPSes
from backend.src.utility import hash_password


#TODO: пройтись mypy в конце

# User crud
async def get_users(db: DPSes, offset: int, limit: int):
    stmt = select(User).offset(offset).limit(limit)
    res = await db.exec(stmt)
    users = res.all()
    return users

async def get_user(db: DPSes, user_id: int):
    user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not user: Exception
    return user

async def create_user(db: DPSes, user_data: UserAdd):
    hashed_password = hash_password(user_data.password)
    extra_data = {'hashed_password': hashed_password}
    db_user = User.model_validate(user_data, update=extra_data)
    await db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)

async def part_update_user(db: DPSes, user_id:int, user_data: UserUpdate):
    db_user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not db_user: Exception
    user = user_data.model_dump(exclude_unset=True)
    extra_data = {}
    if 'password' in user:
        password = user['password']
        hashed_password = hash_password(password)
        extra_data['hashed_password'] = hashed_password
    db_user.sqlmodel_update(user, update=extra_data)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)

async def delete_user(db: DPSes, user_id:int):
    user = await db.get(User, user_id)
    # TODO: Проверка на наличие id - if not user_id: Exception
    await db.delete(user)
    await db.commit()
    return {'ok': True}