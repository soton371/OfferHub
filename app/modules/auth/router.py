from fastapi import APIRouter, status, Depends
from .schema import UserCreate, UserResponse, UserSearch, UserUpdate
from .service import AuthServiceDep


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(data: UserCreate, service: AuthServiceDep):
    print(f'Router create_user data: {data}')
    return await service.create_user(data)

@router.get("/users", response_model=list[UserResponse])
async def get_users(service: AuthServiceDep, search: UserSearch = Depends()):
    print(f'Router get_users search: {search}')
    return await service.get_users(search)

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, service: AuthServiceDep):
    print(f'Router delete_user data: {id}')
    result = await service.delete_user(id)
    return {"detail": f"User {result.name} deleted successfully"}

@router.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, data: UserUpdate, service: AuthServiceDep):
    print(f'Router update_user data: {id}')
    result = await service.update_user(id, data)
    return {"detail": f"User {result.name} updated successfully"}
