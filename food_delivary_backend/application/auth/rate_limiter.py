import time
import uuid
from fastapi import Request, HTTPException
from redis_client import redis_client

def get_client_ip(request:Request):
    return request.client.host

async def rete_limit(request:Request):
    ip=get_client_ip(request)
    key=f"rate_limit:login:{ip}"

    now=time.time()
    cutoff=now-60

    await redis_client.zremrangebyscore(key, 0, cutoff)

    count = await redis_client.zcard(key)
    if count>=5:
        raise HTTPException(
            status_code=429,
            detail="too many requests, please try again later"
        )

    request_id = str(uuid.uuid4())
    await redis_client.zadd(key,{request_id:now})
    await redis_client.expire(key, 60)
