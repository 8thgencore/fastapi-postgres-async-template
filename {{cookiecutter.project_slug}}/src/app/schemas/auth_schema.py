from typing import Any

from pydantic import BaseModel, EmailStr, Field, validator


class IAuthLogin(BaseModel):
    """Authentication Input Schema"""

    email: EmailStr
    password: str

    @validator("email", pre=True, check_fields=False, always=True)
    def validate_email(cls, value: str, values: Any) -> EmailStr():
        return value.lower()


class IAuthRegister(BaseModel):
    """Registration Input Schema"""

    email: EmailStr
    username: str
    password: str

    @validator("email", pre=True, check_fields=False, always=True)
    def validate_email(cls, value: str, values: Any) -> EmailStr():
        return value.lower()


class IAuthChangePassword(BaseModel):
    """ChangePassword Input Schema"""

    current_password: str = Field(description="Current password of a user")
    new_password: str = Field(description="New password of a user")
