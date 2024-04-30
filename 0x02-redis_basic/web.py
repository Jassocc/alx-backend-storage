#!/usr/bin/env python3
"""
A module for caching and tracking
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""
instance of redis module
"""


def data_cacher(method: Callable) -> Callable:
    """
    caches output data
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        wrapper function for caching
        """
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}')
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    returns the content of url's
    """
    return requests.get(url).text
