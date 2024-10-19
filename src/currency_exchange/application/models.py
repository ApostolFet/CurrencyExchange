from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from currency_exchange.domain.models import Currency, CurrencyId, ExchangeRate


@dataclass
class CreateCurrency:
    name: str
    code: str
    sign: str


@dataclass
class CurrencyDTO:
    id: CurrencyId
    name: str
    code: str
    sign: str

    @classmethod
    def from_domain(cls, currency: Currency) -> Self:
        return cls(
            id=currency.id,
            name=currency.name.value,
            code=currency.code.value,
            sign=currency.sign.value,
        )


@dataclass
class CreateExchangeRateDTO:
    base_currency_code: str
    target_currency_code: str
    rate: Decimal


@dataclass
class ExchangeRateDTO:
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal

    @classmethod
    def from_domain(cls, exchange_rate: ExchangeRate) -> Self:
        base_currency = CurrencyDTO.from_domain(exchange_rate.base_currency)
        target_currency = CurrencyDTO.from_domain(exchange_rate.target_currency)
        return cls(
            baseCurrency=base_currency,
            targetCurrency=target_currency,
            rate=exchange_rate.rate.value,
        )


@dataclass
class ExchangeCurrencyDTO:
    base_currency_code: str
    target_currency_code: str
    amount: Decimal


@dataclass
class ExchangedCurrencyDTO:
    baseCurrency: CurrencyDTO
    targetCurrency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    convertedAmount: Decimal


@dataclass
class GetExchangeRate:
    base_code: str
    target_code: str
