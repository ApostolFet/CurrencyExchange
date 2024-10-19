from collections.abc import Hashable
from dataclasses import dataclass, field
from typing import override
from uuid import UUID, uuid4

from currency_exchange.domain.value_objects import (
    CurrencyCode,
    CurrencyName,
    CurrencySign,
    Rate,
)

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


@dataclass(eq=False)
class Currency(Entity[CurrencyId]):
    name: CurrencyName
    code: CurrencyCode
    sign: CurrencySign
    id: CurrencyId = field(default_factory=uuid4)


@dataclass(eq=False)
class ExchangeRate(Entity[ExchangeRateId]):
    base_currency: Currency
    target_currency: Currency
    rate: Rate
    id: ExchangeRateId = field(default_factory=uuid4)
