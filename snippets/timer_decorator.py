import random
import time
import functools
import asyncio
from typing import Callable, TypeVar, Awaitable, ParamSpec, Union


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def timeit_sync(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
    """Декоратор для замера времени выполнения синхронных функций."""

    @functools.wraps(func)
    def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(f"Function `{func.__name__}` took {total_time:.4f} seconds")
        return result

    return wrapper


def timeit_async(
    func: Callable[F_Spec, Awaitable[F_Return]]
) -> Callable[F_Spec, Awaitable[F_Return]]:
    """Декоратор для замера времени выполнения асинхронных функций."""

    @functools.wraps(func)
    async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        print(f"Function `{func.__name__}` took {total_time:.4f} seconds")
        return result

    return wrapper


@timeit_sync
def slp(t: float) -> float:
    time.sleep(t)
    return t


@timeit_async
async def aslp(t: float) -> float:
    await asyncio.sleep(t)
    return t


async def main() -> list[float]:
    tasks = [asyncio.create_task(aslp(random.uniform(0, 1))) for _ in range(5)]
    await asyncio.gather(*tasks)
    return [t.result() for t in tasks]
    # return await aslp(0.3)


if __name__ == "__main__":
    print(slp(random.uniform(0, 1)))
    print(asyncio.run(main()))
