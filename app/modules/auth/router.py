from fastapi import APIRouter, status, Depends
from .schema import UserCreate, UserResponse, UserSearch
from .service import AuthServiceDep


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(data: UserCreate, service: AuthServiceDep):
    print(f'Router User data: {data}')
    return await service.register(data)

@router.get("/users", response_model=list[UserResponse])
async def get_users(service: AuthServiceDep, search: UserSearch = Depends()):
    print(f'Router get_users search: {search}')
    return await service.get_users(search)

