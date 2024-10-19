import functools
import json
from datetime import date, datetime
from typing import Union
from fastapi import Response

from app.init import redis_manager


def data_cache(exp: int = 0):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            allowed_types = Union[str, int, float, bool, date, datetime]

            _kwargs = kwargs.values()
            _kwargs = [str(value) for value in _kwargs if isinstance(value, allowed_types)]
            cache_key = f"{func.__name__}:{''.join(_kwargs)}"

            response: Response = kwargs.get("response")

            if response.headers.get("API-Cache-Key") == cache_key:
                data = {"status": True, "data": response.headers.get("API-Cache-Value")}
                return data
            elif key_value := await redis_manager.get(cache_key):
                data = json.loads(key_value)
                return {"status": True, "data": data}
            else:
                data = await func(*args, **kwargs)
                json_data = json.dumps([value.model_dump() for value in data["data"]])
                await redis_manager.set(cache_key, json_data, expire=exp)
                headers_cache = {
                    "Cache-Control": f"max-age={exp}",
                    "API-Cache-Key": f"{cache_key}",
                    "API-Cache-Value": f"{json_data}",
                }
                response.headers.update(headers_cache)
                return data

        return wrapper

    return decorator
