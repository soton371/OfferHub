import redis.asyncio as redis
from fastapi import HTTPException, status
from app.core.settings import settings

class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    async def store_redis(self, key: str, value: str, ttl: int = 180):
        try:
            await self.redis_client.setex(key, ttl, value)
        except Exception as error:
            # In production, you'd log the 'error' here
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store data in cache"
            )

    async def get_redis(self, key: str) -> str | None:
        try:
            return await self.redis_client.get(key)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve data from cache"
            )

    async def delete_redis(self, key: str):
        try:
            await self.redis_client.delete(key)
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete data from cache"
            )

redis_client = RedisClient()
