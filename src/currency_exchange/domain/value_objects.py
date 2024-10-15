from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import override


@dataclass(frozen=True)
class ValueObject[T](ABC):
    value: T

    def __post_init__(self) -> None:
        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """Raises ValueError if value is invalid"""


@dataclass(frozen=True)
class Rate(ValueObject[Decimal]):
    value: Decimal

    @override
    def _validate(self) -> None:
        if self.value <= 0:
            raise ValueError(f"Rate must be greater then zero, got <{self.value}>")


@dataclass(frozen=True)
class CurrencyCode(ValueObject[str]):
    value: str

    @override
    def _validate(self) -> None:
        count_letters = 3

        if len(self.value) != count_letters:
            raise ValueError(
                f"Currency code must be a {count_letters} letter code, "
                f"got code <{self.value}>"
            )
