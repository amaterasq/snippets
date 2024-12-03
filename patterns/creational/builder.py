"""
- Builder (определяет интерфейс создания частей объекта)
    - AbstractHouseBuilder
- Concrete Builder (определяет сборку конкретных частей)
    - WoodHouseConcreteBuilder, StoneHouseConcreteBuilder
- Product (определяет строящийся сложный объект)
    - WoodHouse, StoneHouse
- Director (отвечает только за выполнение этапов строительства в определенной последовательности, необязателен)
    - HouseDirector

Theory: https://refactoring.guru/design-patterns/builder
Example: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Builder-Pattern

"""

from abc import ABC, abstractmethod
from typing import Literal, Self


class AbstractHouseBuilder(ABC):
    """The AbstractHouseBuilder interface specifies methods for creating the different parts of the House objects."""

    @property
    @abstractmethod
    def product(self) -> "House":
        raise NotImplementedError

    @abstractmethod
    def build_roof(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def build_floor(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def build_garage(self) -> Self:
        raise NotImplementedError


ROOF_TYPES = Literal["flexible_tile", "metal_tile", "default_tile"] | None
FLOOR_TYPES = Literal["parquet", "ceramics", "default_floor"] | None
GARAGE_TYPES = Literal["combined_garage", "temporary_garage", "default_garage"] | None


class House:
    def __init__(self, *, roof: ROOF_TYPES = None, floor: FLOOR_TYPES = None, garage: GARAGE_TYPES = None) -> None:
        self._roof = roof
        self._floor = floor
        self._garage = garage

    @property
    def roof(self) -> ROOF_TYPES:
        return self._roof

    @roof.setter
    def roof(self, roof: ROOF_TYPES) -> None:
        self._roof = roof

    @property
    def floor(self) -> FLOOR_TYPES:
        return self._floor

    @floor.setter
    def floor(self, floor: FLOOR_TYPES) -> None:
        self._floor = floor

    @property
    def garage(self) -> GARAGE_TYPES:
        return self._garage

    @garage.setter
    def garage(self, garage: GARAGE_TYPES) -> None:
        self._garage = garage

    def __str__(self) -> str:
        return f"{self.__class__.__name__}:\n\t{self._roof=},\n\t{self._floor=},\n\t{self._garage=}"


class WoodHouseConcreteBuilder(AbstractHouseBuilder):
    _product: House

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = House()

    @property
    def product(self) -> "House":
        product = self._product
        self.reset()
        return product

    def build_roof(self) -> Self:
        self._product.roof = "flexible_tile"
        return self

    def build_floor(self) -> Self:
        self._product.floor = "parquet"
        return self

    def build_garage(self) -> Self:
        self._product.garage = "temporary_garage"
        return self


class StoneHouseConcreteBuilder(AbstractHouseBuilder):
    _product: House

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = House()

    @property
    def product(self) -> "House":
        product = self._product
        self.reset()
        return product

    def build_roof(self) -> Self:
        self._product.roof = "metal_tile"
        return self

    def build_floor(self) -> Self:
        self._product.floor = "ceramics"
        return self

    def build_garage(self) -> Self:
        self._product.garage = "combined_garage"
        return self


class HouseDirector:

    def __init__(self, builder: AbstractHouseBuilder) -> None:
        self._builder = builder

    @property
    def builder(self) -> AbstractHouseBuilder:
        return self._builder

    def build_house_without_garage(self) -> House:
        self.builder.build_floor().build_roof()
        return self._builder.product

    def build_full_house(self) -> House:
        self.builder.build_roof().build_floor().build_garage()
        return self._builder.product


if __name__ == "__main__":
    wood_house = HouseDirector(builder=WoodHouseConcreteBuilder()).build_full_house()
    stone_house = HouseDirector(builder=StoneHouseConcreteBuilder()).build_full_house()
    print(wood_house)
    print(stone_house)

    # if not use `reset`, old object affected on director
    d = HouseDirector(WoodHouseConcreteBuilder())
    wh = d.build_house_without_garage()
    wh2 = d.build_full_house()
    print(wh)
    print(wh2)

    # Builder pattern can be used without a Director class.
    stone_house_without_director = StoneHouseConcreteBuilder().build_floor().build_garage().build_roof().product
    print(stone_house_without_director)
