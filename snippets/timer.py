import random
import time
import functools
import asyncio
from typing import Any, Callable, TypeVar, Awaitable


F = TypeVar("F", bound=Callable[..., Any] | Callable[..., Awaitable[Any]])

def timeit(func: F) -> F:
    """Декоратор для замера времени выполнения синхронных/асинхронных callable."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()

        async def async_wrapper() -> Any:
            result = await func(*args, **kwargs)
            log_time()
            return result

        def sync_wrapper() -> Any:
            result = func(*args, **kwargs)
            log_time()
            return result

        def log_time():
            total_time = time.perf_counter() - start_time
            print(f'Function `{func.__name__}` took {total_time:.4f} seconds')

        return async_wrapper() if asyncio.iscoroutinefunction(func) else sync_wrapper()
    return wrapper


@timeit
def slp(t: float) -> float:
    time.sleep(t)
    return t


@timeit
async def aslp(t: float) -> float:
    await asyncio.sleep(t)
    return t


async def main() -> list:
    tasks = [asyncio.create_task(aslp(random.uniform(0, 1))) for _ in range(5)]
    await asyncio.gather(*tasks)
    return [t.result() for t in tasks]


if __name__ == "__main__":
    print(slp(random.uniform(0, 1)))
    print(asyncio.run(main()))



