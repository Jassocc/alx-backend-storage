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
    def invoker(url):
        """
        wrapper function for caching
        """
        key = "cached:" + url
        cached_value = redis_store.get(key)
        if cached_value:
            return cached_value.decode('utf-8')
        key_count = "count:" + url
        html_c = method(url)
        redis_store.incr(key_count)
        redis_store.set(key, html_c, ex=10)
        redis_store.expire(key, 10)
        return html_c
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    returns the content of url's
    """
    return requests.get(url).text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
