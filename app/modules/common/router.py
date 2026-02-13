from fastapi import APIRouter, status
from app.modules.common.service import CommonServiceDep
from app.modules.common.schema import SendOtpRequest, VerifyOtpRequest, SendOtpResponse, VerifyOtpResponse

router = APIRouter(prefix='/common', tags=['Common'])

@router.post("/send-otp", response_model=SendOtpResponse, status_code=status.HTTP_200_OK)
async def send_otp(data: SendOtpRequest, service: CommonServiceDep):
    return await service.send_otp(data)

@router.post("/verify-otp", response_model=VerifyOtpResponse, status_code=status.HTTP_200_OK)
async def verify_otp(data: VerifyOtpRequest, service: CommonServiceDep):
    return await service.verify_otp(data)
