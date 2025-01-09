"""Generic functions in python with single-dispatching"""

from functools import singledispatch


class Biba:
    def __init__(self, salary: float):
        self._salary = salary

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, salary: float) -> None:
        self._salary = salary


class Boba:
    def __init__(self, salary: str) -> None:
        self._salary = salary

    @property
    def salary(self) -> str:
        return self._salary

    @salary.setter
    def salary(self, salary: str) -> None:
        self._salary = salary


class Buba:
    def __init__(self, salary: list[float]) -> None:
        self._salary = salary

    @property
    def salary(self) -> list[float]:
        return self._salary

    @salary.setter
    def salary(self, salary: list[float]) -> None:
        self._salary = salary


@singledispatch
def pay_salary(salary: Biba | Boba | Buba, money: float | str | list[float]) -> None:
    raise NotImplementedError(f"Unsupported type: {type(salary)}")


@pay_salary.register(Biba)
def pay_biba(biba: Biba, money: float) -> None:
    biba.salary = biba.salary + money


@pay_salary.register(Boba)
def pay_boba(buba: Boba, money: str) -> None:
    buba.salary = f"{buba.salary}${money}"


@pay_salary.register(Buba)
def pay_buba(buba: Buba, money: list[float]) -> None:
    buba.salary.extend(money)


if __name__ == "__main__":
    biba = Biba(0)
    boba = Boba("0")
    buba = Buba([])

    pay_salary(biba, 10)
    pay_salary(None, 10)
    pay_salary(boba, "10")
    pay_salary(buba, [10])

    print(biba.salary)
    print(boba.salary)
    print(buba.salary)
