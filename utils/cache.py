import redis
import json
import hashlib
from utils import logger
from typing import Any, Optional

redis_client = None
try:
     redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
     redis_client.ping()
     logger.info("Redis cache connected.")
except:
     redis_client = None
     logger.info("Redis not available")

cache ={}

def get_file_hash(file_paths: str) -> str:
        return hashlib.md5(file_paths.read()).hexdigest()

def cache_get(key: str) -> Optional[Any]:
    if redis_client:
         data = redis_client.get(key)
         return json.loads(data) if data else None
    return cache.get(key)

def cache_set(key: str, data: Any, expire_seconds: int = 7*86400):
    if redis_client:
         redis_client.setex(key, expire_seconds, json.dumps(data))
    else:
         cache[key] = data