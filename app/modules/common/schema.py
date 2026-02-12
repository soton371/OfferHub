from pydantic import BaseModel, EmailStr, field_validator

class SendOtpRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip()


class SendOtpResponse(BaseModel):
    detail: str

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str

    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("OTP is required")
        return v.strip()


class VerifyOtpResponse(BaseModel):
    token: str
    

