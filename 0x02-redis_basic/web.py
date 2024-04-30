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


def data_cacher(method):
    """
    caches output data
    """
    @wraps(method)
    def invoker(url: str):
        """
        wrapper function for caching
        """
        cach_con = redis_store.get(f"cached:{url}")
        if cach_con:
            return cach_con.decode('utf-8')
        con = method(url)
        redis_store.setex(f"cached:{url}", 10, con)
        return con
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    returns the content of url's
    """
    counter = redis_store.incr(f"count:{url}")
    con = requests.get(url).text
    return con
