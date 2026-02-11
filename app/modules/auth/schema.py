from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str

    @field_validator('email')
    @classmethod
    def email_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Email cannot be empty')
        return v.strip()


class UserResponse(UserCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSearch(BaseModel):
    page: int = 1
    limit: int = 10
    email: str | None = None
    sort_by: str = "created_at"
    sort_order: str = "desc"

    @field_validator('limit')
    @classmethod
    def limit_must_be_valid(cls, v: int) -> int:
        if v < 1:
            return 10
        if v > 100:
            return 100
        return v
