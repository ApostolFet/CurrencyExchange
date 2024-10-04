from dataclasses import dataclass
from typing import override

from currency_exchange.domain.value_objects import CurrencyCode, Rate

type CurrencyId = int
type ExchangeRateId = int


@dataclass
class Currency:
    name: str
    code: CurrencyCode
    sign: str
    id: CurrencyId | None = None

    @override
    def __eq__(self, value: object, /) -> bool:
        cls = self.__class__
        if isinstance(value, cls):
            return value.id == self.id
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class ExchangeRate:
    base_currency: Currency
    target_currency: Currency
    rate: Rate
    id: ExchangeRateId | None = None

    @override
    def __eq__(self, value: object, /) -> bool:
        cls = self.__class__
        if isinstance(value, cls):
            return value.id == self.id
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.id)
