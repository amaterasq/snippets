from collections.abc import Iterable
from typing import TypeVar

from itertools import batched, islice

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterable[list[T]]:
    """Yield successive n-sized chunks from items (itertools.batched)."""
    buffer = []
    for item in items:
        buffer.append(item)
        if len(buffer) != size:
            continue
        yield buffer
        buffer = []
    if buffer:
        yield buffer

    # second vers
    # it = iter(items)
    # while chunk := tuple(islice(it, size)):
    #     yield chunk


if __name__ == "__main__":
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunked([], 2)) == []
    assert list(chunked([1], 2)) == [[1]]

    assert list(batched([1, 2, 3, 4, 5], 2)) == [(1, 2), (3, 4), (5,)]
