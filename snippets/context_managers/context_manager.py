import asyncio
from contextlib import asynccontextmanager, AsyncExitStack
from types import TracebackType
from typing import Literal, Self, Type

BROWSER_NAME = Literal["Safari", "Chrome", "Brave"]


class Browser:
    def __init__(self, name: BROWSER_NAME):
        self.name = name

    async def find(self, query: str) -> str:
        await asyncio.sleep(1.5)
        return f"Result by search {query} on {self.name} is ..."

    async def __aenter__(self) -> Self:
        print(f"Before async context manager (magic method): opening browser {self.name}")
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        print(f"After async context manager (magic method): closing browser: {self.name}")


@asynccontextmanager
async def get_browser(browser_name: BROWSER_NAME):
    print(f"Before async context manager (contextlib): opening browser {browser_name}")
    try:
        yield Browser(browser_name)
    finally:
        print(f"After async context manager (contextlib): closing browser: {browser_name}")


async def main():
    # через asynccontextmanager
    async with get_browser("Chrome") as browser:
        print(await browser.find("42"))

    # через aenter/aexit
    async with Browser("Safari") as browser:
        print(await browser.find("42"))

    # если мы не знаем, сколько менеджеров нужно открыть - но все нужно централизованно закрыть
    async with AsyncExitStack() as stack:
        for name in ["Safari", "Chrome", "Brave"]:
            browser = await stack.enter_async_context(get_browser(name))
            print(await browser.find("42"))


if __name__ == "__main__":
    asyncio.run(main())
