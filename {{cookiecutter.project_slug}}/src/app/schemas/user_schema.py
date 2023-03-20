from enum import Enum
from uuid import UUID

from app.models.user_model import UserBase
from app.schemas.role_schema import IRoleRead
from app.utils.partial import optional


class IUserCreate(UserBase):
    password: str | None

    class Config:
        hashed_password = None


# All these fields are optional
@optional
class IUserUpdate(UserBase):
    pass


class IUserRead(UserBase):
    id: UUID
    role: IRoleRead | None = None


class IUserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
