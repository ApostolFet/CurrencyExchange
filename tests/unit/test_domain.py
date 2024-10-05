from decimal import Decimal

import pytest

from currency_exchange.domain.exceptions import (
    ExchangeRateCantBeMergeError,
)
from currency_exchange.domain.models import Currency, ExchangeRate
from currency_exchange.domain.services import (
    exchange_currency,
    merge_exchange_rate,
    reverse_exchange_rate,
)
from currency_exchange.domain.value_objects import CurrencyCode, Rate


def test_create_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")

    rate_ruble_dollar = Decimal(100)
    expected_result_rate = Rate(rate_ruble_dollar)

    result_exchange = ExchangeRate(ruble, dollar, Rate(rate_ruble_dollar))

    assert result_exchange.rate == expected_result_rate
    assert result_exchange.base_currency == ruble
    assert result_exchange.target_currency == dollar


def test_exchange_currency() -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    rate = Decimal(30)
    exchange_rate = ExchangeRate(ruble, dollar, Rate(rate))
    amount = Decimal(1_000)
    expected_result = Decimal(30_000)

    result = exchange_currency(exchange_rate, amount)

    assert result == expected_result


def test_reverse_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    rate = Decimal(100)

    exchange_rate = ExchangeRate(ruble, dollar, Rate(rate))
    expected_result_rate = Rate(Decimal("0.01"))

    result_excchange = reverse_exchange_rate(exchange_rate)

    assert result_excchange.rate == expected_result_rate
    assert result_excchange.base_currency == dollar
    assert result_excchange.target_currency == ruble


def test_merge_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")

    rate_ruble_dollar = Decimal(100)
    exchange_rate_ruble_dollar = ExchangeRate(ruble, dollar, Rate(rate_ruble_dollar))
    rate_dollar_euro = Decimal(2)
    exchange_rate_dollar_euro = ExchangeRate(dollar, euro, Rate(rate_dollar_euro))
    expected_result_rate = Rate(Decimal(200))

    result_exchange = merge_exchange_rate(
        exchange_rate_ruble_dollar,
        exchange_rate_dollar_euro,
    )

    assert result_exchange.rate == expected_result_rate
    assert result_exchange.base_currency == ruble
    assert result_exchange.target_currency == euro


def test_cant_merge_non_related_exchange_rate() -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")
    sterling = Currency("Pound Sterling", CurrencyCode("GBP"), "")

    rate_ruble_dollar = Decimal(100)
    exchange_rate_ruble_dollar = ExchangeRate(ruble, dollar, Rate(rate_ruble_dollar))
    rate_euro_sterling = Decimal(2)
    exchange_rate_euro_sterling = ExchangeRate(sterling, euro, Rate(rate_euro_sterling))

    with pytest.raises(ExchangeRateCantBeMergeError):
        merge_exchange_rate(exchange_rate_ruble_dollar, exchange_rate_euro_sterling)


@pytest.mark.parametrize(
    ("currency_code"),
    [
        ("RU"),
        ("RUBS"),
        ("R"),
        ("DOLLAR"),
    ],
)
def test_cant_create_invalid_currency_code(currency_code: str) -> None:
    with pytest.raises(ValueError, match="Currency code must be"):
        CurrencyCode(currency_code)


@pytest.mark.parametrize(
    ("rate"),
    [
        (Decimal(0)),
        (Decimal(-1)),
        (Decimal(-50)),
    ],
)
def test_cant_create_invalid_rate(rate: Decimal) -> None:
    with pytest.raises(ValueError, match="Rate must be greater then zero"):
        Rate(rate)
