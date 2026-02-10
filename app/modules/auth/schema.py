from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr

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

