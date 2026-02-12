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

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, service: AuthServiceDep):
    print(f'Router delete data: {id}')
    result = await service.delete(id)
    return {"detail": f"User {result.name} deleted successfully"}

@router.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update(id: int, data: UserCreate, service: AuthServiceDep):
    print(f'Router update data: {id}')
    result = await service.update(id, data)
    return {"detail": f"User {result.name} updated successfully"}
