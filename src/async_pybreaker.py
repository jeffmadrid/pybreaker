#-*- coding:utf-8 -*-
from functools import wraps

import pybreaker


class AsyncCircuitBreaker(pybreaker.CircuitBreaker):

    async def call_async(self, func, *args, **kwargs):
        with self._lock:
            return await self.state.call_async(func, *args, **kwargs)

    def __call__(self, *call_args, **call_kwargs):

        def _outer_wrapper(func):
            @wraps(func)
            async def _inner_wrapper(*args, **kwargs):
                return await self.call_async(func, *args, **kwargs)
            return _inner_wrapper

        if call_args:
            return _outer_wrapper(*call_args)
        return _outer_wrapper


