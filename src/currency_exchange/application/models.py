from dataclasses import dataclass
from decimal import Decimal

from currency_exchange.domain.models import Currency


@dataclass
class CreateCurrency:
    name: str
    code: str
    sign: str


@dataclass
class ExchangeRateDTO:
    base_currency_code: str
    target_currency_code: str
    rate: Decimal


@dataclass
class ExchangeCurrencyDTO:
    base_currency_code: str
    target_currency_code: str
    amount: Decimal


@dataclass
class ExchangedCurrencyDTO:
    base_currency: Currency
    target_currency: Currency
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal


@dataclass
class GetExchangeRate:
    base_code: str
    target_code: str
