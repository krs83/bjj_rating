from typing import Literal
from sqlmodel import Field, SQLModel
from pydantic import EmailStr, ConfigDict

ROLES = Literal[1,2,3,4]

USER: ROLES = 1
COACH: ROLES = 2
ADMIN: ROLES = 3
SUPER_ADMIN: ROLES = 4

class UserBase(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True)
    role: int = Field(default=USER, nullable=False)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=200)


class UserAdd(UserBase):
    password: str = Field(min_length=3)

class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
