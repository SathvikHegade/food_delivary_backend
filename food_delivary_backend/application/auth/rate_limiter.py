import time
import uuid
from fastapi import Request, HTTPException
from redis_client import redis_client

def get_client_ip(request:Request):
    return request.client.host

async def check_rate_limit(request:Request):
    ip=get_client_ip(request)
    key=f"rate_limit:login:{ip}"
    block_key=f"login:block:{ip}"
    blocked=await redis_client.exists(block_key)

    if blocked:
        raise HTTPException(
            status_code=429,
            detail="Blocked:-Too many failed login attempts. Please try again later."
        )



async def record_failed_attempt(request: Request):
    ip = get_client_ip(request)

    key = f"rate_limit:login:{ip}"
    block_key = f"login:block:{ip}"

    now = time.time()
    cutoff = now - 60
    request_id = str(uuid.uuid4())

    script = """
    redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, ARGV[1])

    redis.call('ZADD', KEYS[1], ARGV[2], ARGV[3])

    redis.call('EXPIRE', KEYS[1], 60)

    local count = redis.call('ZCARD', KEYS[1])

    if count >= 5 then
        redis.call('SET', KEYS[2], '1', 'EX', 60)
        return 1
    end

    return 0
    """

    result = await redis_client.eval(
        script,
        2,
        key,
        block_key,
        cutoff,
        now,
        request_id
    )

    return result == 1
