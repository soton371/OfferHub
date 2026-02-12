from redis import Redis

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)


def storeRedis(key: str, value: str, ttl: int = 180)-> bool:
    try:
        redis_client.setex(key, ttl, value)
        return True
    except Exception as error:
        print(f"storeRedis error: {error}")
        return False

def getRedis(key: str | None)-> (str | None):
    if key is None:
        return None
    return redis_client.get(key)

def deleteRedis(key: str):
    redis_client.delete(key)
