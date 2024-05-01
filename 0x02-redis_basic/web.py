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
    def invoker(url: str) -> str:
        """
        wrapper function for caching
        """
        cached_con = redis_store.get(f"cached:{url}")
        if cached_con:
            return cached_con.decode('utf-8')
        content = method(url)
        redis_store.setex(f"cached:{url}", 10, content)
        redis_store.incr(f"count:{url}")
        return content
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    returns the content of url's
    """
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
