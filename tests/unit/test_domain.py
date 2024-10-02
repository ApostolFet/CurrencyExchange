from decimal import Decimal

from currency_exchange.domain.models import Currency
from currency_exchange.domain.services import (
    create_exchange_rate,
    exchange_currency,
    merge_exchange_rate,
    reverse_exchange_rate,
)


def test_exchange_currency() -> None:
    ruble = Currency("Russian Ruble", "RUB", "", 0)
    dollar = Currency("US Dollar", "USD", "", 1)
    rate = Decimal(30)
    exchange_rate = create_exchange_rate(ruble, dollar, rate)
    amount = Decimal(1_000)
    expected_result = Decimal(30_000)

    result = exchange_currency(exchange_rate, amount)

    assert result == expected_result


def test_reverse_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", "RUB", "", 0)
    dollar = Currency("US Dollar", "USD", "", 1)
    rate = Decimal(100)

    exchange_rate = create_exchange_rate(ruble, dollar, rate)
    expected_result_rate = Decimal("0.01")

    result_excchange = reverse_exchange_rate(exchange_rate)

    assert result_excchange.rate == expected_result_rate
    assert result_excchange.base_currency_id == dollar.id
    assert result_excchange.target_currency_id == ruble.id


def test_merge_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", "RUB", "", 0)
    dollar = Currency("US Dollar", "USD", "", 1)
    euro = Currency("Euro", "EUR", "", 2)

    rate_ruble_dollar = Decimal(100)
    exchange_rate_ruble_dollar = create_exchange_rate(ruble, dollar, rate_ruble_dollar)
    rate_dollar_euro = Decimal(2)
    exchange_rate_dollar_euro = create_exchange_rate(dollar, euro, rate_dollar_euro)
    expected_result_rate = Decimal(200)

    result_excchange = merge_exchange_rate(
        exchange_rate_ruble_dollar,
        exchange_rate_dollar_euro,
    )

    assert result_excchange.rate == expected_result_rate
    assert result_excchange.base_currency_id == ruble.id
    assert result_excchange.target_currency_id == euro.id
