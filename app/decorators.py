import asyncio
import logging
from collections.abc import Awaitable, Callable
from functools import wraps

from errors import RetryingError

type Func[T] = Callable[..., Awaitable[T]]
type Wrapper[T] = Callable[..., T]
type Decorator[T] = Callable[Func[T], Wrapper[T]]


def retries[T](times: int = 3) -> Decorator[T]:
    def decorator(func: Func[T]) -> Wrapper[T]:
        @wraps(func)
        async def wrapper(*args: ..., **kwargs: ...) -> T:
            attempts = 0
            while True:
                try:
                    attempts += 1
                    return await  func(*args, **kwargs)
                except RetryingError:
                    if attempts >= times:
                        raise

                    logging.exception("Retrying")
                    await asyncio.sleep(0.5)

        return wrapper

    return decorator
