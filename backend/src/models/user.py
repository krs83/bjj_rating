from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True)


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
