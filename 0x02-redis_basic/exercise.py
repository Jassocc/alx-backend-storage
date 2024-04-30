#!/usr/bin/env python3
"""
script for the excercise python file
"""
import uuid
import redis
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    tracks the amount of calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        returns the given method
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    tracks details of calls
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        returns all outputs
        """
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        outp = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, outp)
        return outp
    return invoker


def replay(fn: Callable) -> None:
    """
    Shows the call history
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    input_key = '{}:inputs'.format(fxn_name)
    output_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(input_key, 0, -1)
    fxn_outputs = redis_store.lrange(output_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output))


class Cache:
    """
    class for caching stored objects
    """
    def __init__(self) -> None:
        """
        initializes objects
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores values to a data storage db
        """
        d_key = str(uuid.uuid4())
        self._redis.set(d_key, data)
        return d_key

    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        gets value from redis data
        """
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        gets a string from redis
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        gets an int value from redis
        """
        return self.get(key, lambda x: int(x))
