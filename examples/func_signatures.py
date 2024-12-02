from typing import Iterable


def only_args(*args: float) -> float:
    return sum(args)


def only_kwargs(*, a: str, b: str) -> str:
    return f"{a}:{b}"


def two_args_two_kwargs(a: int, b: int, *, c: int, d: int) -> None:
    """c, d - только именованные."""
    # two_args_two_kwargs(a=1, b=2, c=3, d=4) - ok
    # two_args_two_kwargs(1, 2, c=3, d=4) - ok
    # two_args_two_kwargs(1, 2, 3, 4) - not
    print(f"args: {a}, {b}")
    print(f"kwargs: {c}, {d}")


def two_args_two_kwargs2(a: int, b: int, /, c: int, d: int) -> None:
    """a, b - только позиционные."""
    # two_args_two_kwargs2(1, 2, c=3, d=4) - ok
    # two_args_two_kwargs2(1, 2, 3, 4) - ok
    # two_args_two_kwargs2(a=1, b=2, c=3, d=4) - not
    print(f"args: {a}, {b}")
    print(f"kwargs: {c}, {d}")
