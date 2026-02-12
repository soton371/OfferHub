from fastapi import APIRouter, status, Depends
from .schema import UserCreate, UserResponse, UserSearch, UserUpdate
from .service import AuthServiceDep


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(data: UserCreate, service: AuthServiceDep):
    print(f'Router create_user data: {data}')
    return await service.create_user(data)

@router.get("/", response_model=list[UserResponse])
async def get_users(service: AuthServiceDep, search: UserSearch = Depends()):
    print(f'Router get_users search: {search}')
    return await service.get_users(search)

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, service: AuthServiceDep):
    print(f'Router get_user data: {id}')
    return await service.get_user(id)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, service: AuthServiceDep):
    print(f'Router delete_user data: {id}')
    result = await service.delete_user(id)
    return {"detail": f"User {result.name} deleted successfully"}

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, data: UserUpdate, service: AuthServiceDep):
    print(f'Router update_user data: {id}')
    result = await service.update_user(id, data)
    return {"detail": f"User {result.name} updated successfully"}
