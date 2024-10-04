from decimal import Decimal

from currency_exchange.domain.exceptions import (
    CurrencyDontHaveIdError,
    ExchangeRateCantBeMergeError,
)
from currency_exchange.domain.models import Currency, ExchangeRate
from currency_exchange.domain.value_objects import Rate


def create_exchange_rate(
    base_currency: Currency,
    target_currency: Currency,
    rate: Decimal,
) -> ExchangeRate:
    if base_currency.id is None or target_currency.id is None:
        raise CurrencyDontHaveIdError()
    return ExchangeRate(base_currency, target_currency, Rate(rate))


def exchange_currency(exchange_rate: ExchangeRate, amount: Decimal) -> Decimal:
    return exchange_rate.rate.value * amount


def reverse_exchange_rate(exchange_rate: ExchangeRate) -> ExchangeRate:
    reverse_rate_value = 1 / exchange_rate.rate.value
    reverse_rate = Rate(reverse_rate_value)
    return ExchangeRate(
        exchange_rate.target_currency,
        exchange_rate.base_currency,
        reverse_rate,
    )


def merge_exchange_rate(
    base_exchange_rate: ExchangeRate,
    target_exchange_rate: ExchangeRate,
) -> ExchangeRate:
    if base_exchange_rate.target_currency != target_exchange_rate.base_currency:
        raise ExchangeRateCantBeMergeError("Cant merge non related exchange rate")

    merged_rate = base_exchange_rate.rate.value * target_exchange_rate.rate.value

    return ExchangeRate(
        base_exchange_rate.base_currency,
        target_exchange_rate.target_currency,
        rate=Rate(merged_rate),
    )
