from app.modules.common.schema import SendOtpRequest, SendOtpResponse, VerifyOtpRequest, VerifyOtpResponse
from app.db.redis_db import redis_client
from fastapi import HTTPException, status, Depends
from app.modules.user.repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import Annotated
import random
import string


class CommonService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def send_otp(self, data: SendOtpRequest):
        exist_user = await self.user_repository.get_by_email(data.email)
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        otp = ''.join(random.choices(string.digits, k=6))
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

async def get_common_service(db: AsyncSession = Depends(get_db)) -> CommonService:
    return CommonService(db)

CommonServiceDep = Annotated[CommonService, Depends(get_common_service)]
