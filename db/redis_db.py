import os
import redis
from settings import redis_host,redis_port
r = redis.Redis(
        host = redis_host,
        port=int (redis_port),
        decode_responses=True  # Đảm bảo rằng các giá trị được giải mã từ byte sang string
)
