from decimal import Decimal

from currency_exchange.domain.exceptions import CurrencyDontHaveIdError
from currency_exchange.domain.models import Currency, ExchangeRate


def create_exchange_rate(
    base_currency: Currency,
    target_currency: Currency,
    rate: Decimal,
) -> ExchangeRate:
    if base_currency.id is None or target_currency.id is None:
        raise CurrencyDontHaveIdError()
    return ExchangeRate(base_currency.id, target_currency.id, rate)


def exchange_currency(exchange_rate: ExchangeRate, amount: Decimal) -> Decimal:
    return exchange_rate.rate * amount


def reverse_exchange_rate(exchange_rate: ExchangeRate) -> ExchangeRate:
    reverse_rate = 1 / exchange_rate.rate
    return ExchangeRate(
        exchange_rate.target_currency_id,
        exchange_rate.base_currency_id,
        reverse_rate,
    )


def merge_exchange_rate(
    base_exchange_rate: ExchangeRate,
    target_exchange_rate: ExchangeRate,
) -> ExchangeRate:
    merged_rate = base_exchange_rate.rate * target_exchange_rate.rate
    return ExchangeRate(
        base_exchange_rate.base_currency_id,
        target_exchange_rate.target_currency_id,
        rate=merged_rate,
    )
