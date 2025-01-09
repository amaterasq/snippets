import random
import time
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def retry(
    count: int = 1,
    delay_sec: float = 0.5,
    backoff: float = 1.0,  # off by default
) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, F_Return | None]]:
    """
    Декоратор для повторной попытки выполнения функции.

    :param count: Количество попыток.
    :param delay_sec: Начальная задержка между попытками.
    :param backoff: Множитель для экспоненциального увеличения задержки между попытками.
    """

    def wrapper(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return | None]:
        @wraps(func)
        def inner(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return | None:
            curr_delay = delay_sec
            for attempt in range(1, count + 1):
                try:
                    res = func(*args, **kwargs)
                except Exception as e:
                    print(f"Failed {attempt=} with `{e}`. Retrying in {curr_delay} seconds...")
                    time.sleep(curr_delay)
                    curr_delay = round(curr_delay * backoff, 1)
                else:
                    print(f"Successfully `{func.__name__} {args, kwargs}` call, {attempt=}")
                    return res
            print(f"Failed `{func.__name__} {args, kwargs}` with {count} attempts")
            return None

        return inner

    return wrapper


@retry(count=5, delay_sec=0.7, backoff=1.4)
def random_err(a: float, b: float = 2) -> float:
    if random.uniform(0, 1) < 0.7:
        raise ValueError("r error")
    return a + b


if __name__ == "__main__":
    print(random_err(1, b=2))
