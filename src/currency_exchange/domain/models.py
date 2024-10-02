from dataclasses import dataclass
from decimal import Decimal

type CurrencyId = int
type ExchangeRateId = int


@dataclass
class Currency:
    name: str
    code: str
    sign: str
    id: CurrencyId | None = None


@dataclass
class ExchangeRate:
    base_currency_id: CurrencyId
    target_currency_id: CurrencyId
    rate: Decimal
    id: ExchangeRateId | None = None
