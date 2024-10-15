from decimal import Decimal
from sqlite3 import Connection

import pytest

from currency_exchange.application.exceptions import (
    CurrencyCodeAlreadyExistsError,
    ExchangeRateAlreadyExistsError,
)
from currency_exchange.domain.models import Currency, ExchangeRate
from currency_exchange.domain.value_objects import CurrencyCode, Rate
from currency_exchange.infrastructure.database.repo import (
    SQLiteCurrencyRepository,
    SQLiteExchangeRateRepository,
)


def test_get_currency_by_code(connection_in_memory_db: Connection) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")

    repo = SQLiteCurrencyRepository(connection_in_memory_db)
    repo.add(ruble)
    repo.add(dollar)
    repo.add(euro)
    result = repo.get_by_code("EUR")

    assert result == euro


def test_get_pair_currency(connection_in_memory_db: Connection) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")

    repo = SQLiteCurrencyRepository(connection_in_memory_db)
    repo.add(ruble)
    repo.add(dollar)
    repo.add(euro)
    result = repo.get_pair(("EUR", "RUB"))

    assert result == (euro, ruble)


def test_get_all_currencies(connection_in_memory_db: Connection) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")

    repo = SQLiteCurrencyRepository(connection_in_memory_db)
    repo.add(ruble)
    repo.add(dollar)
    repo.add(euro)
    result = repo.get_all()

    assert result == [ruble, dollar, euro]


def test_failed_adding_existing_code(
    connection_in_memory_db: Connection,
) -> None:
    ruble_1 = Currency("Russian Ruble 1", CurrencyCode("RUB"), "")
    ruble_2 = Currency("Russian Ruble 2", CurrencyCode("RUB"), "")

    currency_repo = SQLiteCurrencyRepository(connection_in_memory_db)
    currency_repo.add(ruble_1)

    with pytest.raises(CurrencyCodeAlreadyExistsError):
        currency_repo.add(ruble_2)


def test_get_by_currency_codes_exchange_rate(
    connection_in_memory_db: Connection,
) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")
    ruble_dollar_rate = ExchangeRate(ruble, dollar, rate=Rate(Decimal("30")))
    dollar_euro_rate = ExchangeRate(dollar, euro, rate=Rate(Decimal("1.5")))

    currency_repo = SQLiteCurrencyRepository(connection_in_memory_db)
    currency_repo.add(ruble)
    currency_repo.add(dollar)
    currency_repo.add(euro)
    exchange_rate_repo = SQLiteExchangeRateRepository(connection_in_memory_db)
    exchange_rate_repo.add(ruble_dollar_rate)
    exchange_rate_repo.add(dollar_euro_rate)
    result = exchange_rate_repo.get_by_currency_codes("USD", "EUR")

    assert result == dollar_euro_rate
    assert result.rate == dollar_euro_rate.rate


def test_related_exchanges_by_currency_codes(
    connection_in_memory_db: Connection,
) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")
    ruble_dollar_rate = ExchangeRate(ruble, dollar, rate=Rate(Decimal("30")))
    dollar_euro_rate = ExchangeRate(dollar, euro, rate=Rate(Decimal("1.5")))

    currency_repo = SQLiteCurrencyRepository(connection_in_memory_db)
    currency_repo.add(ruble)
    currency_repo.add(dollar)
    currency_repo.add(euro)
    exchange_rate_repo = SQLiteExchangeRateRepository(connection_in_memory_db)
    exchange_rate_repo.add(ruble_dollar_rate)
    exchange_rate_repo.add(dollar_euro_rate)
    result = exchange_rate_repo.get_related_exchanges_by_currency_codes(
        "RUB",
        "EUR",
        "USD",
    )

    assert result == (ruble_dollar_rate, dollar_euro_rate)


def test_get_all_exchanges(
    connection_in_memory_db: Connection,
) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")
    euro = Currency("Euro", CurrencyCode("EUR"), "")
    ruble_dollar_rate = ExchangeRate(ruble, dollar, rate=Rate(Decimal("30")))
    dollar_euro_rate = ExchangeRate(dollar, euro, rate=Rate(Decimal("1.5")))

    currency_repo = SQLiteCurrencyRepository(connection_in_memory_db)
    currency_repo.add(ruble)
    currency_repo.add(dollar)
    currency_repo.add(euro)
    exchange_rate_repo = SQLiteExchangeRateRepository(connection_in_memory_db)
    exchange_rate_repo.add(ruble_dollar_rate)
    exchange_rate_repo.add(dollar_euro_rate)
    result = exchange_rate_repo.get_all()

    assert result == [ruble_dollar_rate, dollar_euro_rate]


def test_failed_adding_existing_exchange_rate(
    connection_in_memory_db: Connection,
) -> None:
    ruble = Currency("Russian Ruble", CurrencyCode("RUB"), "")
    dollar = Currency("US Dollar", CurrencyCode("USD"), "")

    ruble_dollar_rate = ExchangeRate(ruble, dollar, rate=Rate(Decimal("30")))
    dollar_euro_rate = ExchangeRate(ruble, dollar, rate=Rate(Decimal("100")))

    currency_repo = SQLiteCurrencyRepository(connection_in_memory_db)
    currency_repo.add(ruble)
    currency_repo.add(dollar)
    exchange_rate_repo = SQLiteExchangeRateRepository(connection_in_memory_db)
    exchange_rate_repo.add(ruble_dollar_rate)

    with pytest.raises(ExchangeRateAlreadyExistsError):
        exchange_rate_repo.add(dollar_euro_rate)
