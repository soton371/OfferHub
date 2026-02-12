from app.modules.common.schema import SendOtpRequest, SendOtpResponse, VerifyOtpRequest, VerifyOtpResponse
from app.db.redis_db import storeRedis, getRedis, deleteRedis
from fastapi import HTTPException, status

class CommonService:
    def send_otp(self, data: SendOtpRequest):
        otp = '123456'
        result = storeRedis(data.email, otp)
        if result is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to send OTP")
        return SendOtpResponse(detail="OTP sent successfully")

    def verify_otp(self, data: VerifyOtpRequest):
        stored_otp = getRedis(data.email)
        print(f'stored_otp: {stored_otp}')
        if stored_otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found")
        if stored_otp != data.otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        deleteRedis(data.email)
        return VerifyOtpResponse(token="token")


