import time
import pytest
import asyncio
from snippets.timer_decorator import timeit_sync, timeit_async


# Синхронная функция для теста
@timeit_sync
def sync_function(x: float) -> None:
    time.sleep(x)


# Асинхронная функция для теста
@timeit_async
async def async_function(x: float) -> float:
    await asyncio.sleep(x)
    return x


def test_sync_function_time(capfd):
    """
    Тест для синхронной функции.
    Проверяет, что время выполнения синхронной функции выводится корректно.
    """
    sync_function(0.2)

    # Проверяем, что выводится сообщение с временем
    captured = capfd.readouterr()
    assert "Function `sync_function` took" in captured.out
    assert "seconds" in captured.out


@pytest.mark.asyncio
async def test_async_function_time(capfd):
    """Проверяет, что время выполнения асинхронной функции выводится корректно."""
    await async_function(0.2)
    # Проверяем, что выводится сообщение с временем
    captured = capfd.readouterr()
    assert "Function `async_function` took" in captured.out
    assert "seconds" in captured.out


@pytest.mark.asyncio
async def test_async_function_result():
    """Тест для проверки результата выполнения асинхронной функции."""
    result = await async_function(0.3)
    assert result == 0.3


def test_sync_function_result():
    """Тест для проверки результата выполнения синхронной функции."""
    sync_function(1.0)
    # Здесь просто проверяем, что не произошло исключений
    assert True
