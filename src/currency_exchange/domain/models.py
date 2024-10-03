from dataclasses import dataclass

from currency_exchange.domain.value_objects import CurrencyCode, Rate

type CurrencyId = int
type ExchangeRateId = int


@dataclass
class Currency:
    name: str
    code: CurrencyCode
    sign: str
    id: CurrencyId | None = None


@dataclass
class ExchangeRate:
    base_currency_id: CurrencyId
    target_currency_id: CurrencyId
    rate: Rate
    id: ExchangeRateId | None = None
