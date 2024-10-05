from collections.abc import Hashable
from dataclasses import dataclass, field
from typing import override
from uuid import UUID, uuid4

from currency_exchange.domain.value_objects import CurrencyCode, Rate

type CurrencyId = UUID
type ExchangeRateId = UUID


class Entity[T: Hashable]:
    id: T

    @override
    def __eq__(self, value: object, /) -> bool:
        cls = self.__class__
        if isinstance(value, cls) and self.id is not None:
            return value.id == self.id
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Currency(Entity[CurrencyId]):
    name: str
    code: CurrencyCode
    sign: str
    id: CurrencyId = field(default_factory=uuid4)


@dataclass
class ExchangeRate(Entity[ExchangeRateId]):
    base_currency: Currency
    target_currency: Currency
    rate: Rate
    id: ExchangeRateId = field(default_factory=uuid4)
