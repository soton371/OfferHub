from pydantic import BaseModel, EmailStr, field_validator

class SendOtpRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    def validate_email(cls, v):
        if not v.strip():
            raise ValueError("Email is required")
        return v.strip()


class SendOtpResponse(BaseModel):
    detail: str

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class VerifyOtpResponse(BaseModel):
    token: str
    

