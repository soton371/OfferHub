from redis import Redis
from fastapi import HTTPException, status

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)


def storeRedis(key: str, value: str, ttl: int = 180):
    try:
        redis_client.setex(key, ttl, value)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to store OTP")
        

def getRedis(key: str | None)-> (str | None):
    try:
        return redis_client.get(key)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get OTP")

def deleteRedis(key: str):
    try:
        redis_client.delete(key)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete OTP")
