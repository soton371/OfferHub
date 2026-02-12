from app.modules.common.schema import SendOtpRequest, SendOtpResponse, VerifyOtpRequest, VerifyOtpResponse
from app.db.redis_db import redis_client
from fastapi import HTTPException, status

class CommonService:
    async def send_otp(self, data: SendOtpRequest):
        otp = '123456'
        await redis_client.store_redis(data.email, otp)
        return SendOtpResponse(detail="OTP sent successfully")

    async def verify_otp(self, data: VerifyOtpRequest):
        stored_otp = await redis_client.get_redis(data.email)
        print(f'stored_otp: {stored_otp}')
        if stored_otp is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not found")
        if stored_otp != data.otp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        await redis_client.delete_redis(data.email)
        return VerifyOtpResponse(token="token")

common_service = CommonService()
