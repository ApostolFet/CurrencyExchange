from sqlite3 import PARSE_DECLTYPES, Connection, connect

from currency_exchange.application.interactors.currencies import (
    CreateCurrencyInteracotor,
    GetCurrenciesInteractor,
    GetCurrencyInteractor,
)
from currency_exchange.application.interactors.exchange_rates import (
    CreateExchangeRateInteractor,
    ExchangeCurrencyInteractor,
    GetExchangeRateInteractor,
    GetExchangeRatesInteractor,
    UpdateExchangeRateInteractor,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.infrastructure.database.repo import (
    SQLiteCurrencyRepository,
    SQLiteExchangeRateRepository,
)
from simple_di.container import Container
from simple_di.integration import FromSimpleDi


def factory_sqlite_connection() -> Connection:
    connection = connect("currency_exchange.db", detect_types=PARSE_DECLTYPES)
    return connection


def deliter_sqlite_connection(connection: Connection) -> None:
    connection.close()


def factory_sqlite_currency_repo(
    connection: FromSimpleDi[Connection],
) -> CurrencyRepository:
    return SQLiteCurrencyRepository(connection)


def factory_sqlite_exchange_rate_repo(
    connection: FromSimpleDi[Connection],
) -> ExchangeRateRepository:
    return SQLiteExchangeRateRepository(connection)


def factory_create_currency_interactor(
    currency_repo: FromSimpleDi[CurrencyRepository],
) -> CreateCurrencyInteracotor:
    return CreateCurrencyInteracotor(currency_repo)


def factory_get_currencies_interactor(
    currency_repo: FromSimpleDi[CurrencyRepository],
) -> GetCurrenciesInteractor:
    return GetCurrenciesInteractor(currency_repo)


def factory_get_currency_interactor(
    currency_repo: FromSimpleDi[CurrencyRepository],
) -> GetCurrencyInteractor:
    return GetCurrencyInteractor(currency_repo)


def factory_exchange_interactor(
    exchange_rate_repo: FromSimpleDi[ExchangeRateRepository],
) -> ExchangeCurrencyInteractor:
    return ExchangeCurrencyInteractor(exchange_rate_repo, "USD")


def factory_get_exchange_rates_interactor(
    exchange_rate_repo: FromSimpleDi[ExchangeRateRepository],
) -> GetExchangeRatesInteractor:
    return GetExchangeRatesInteractor(exchange_rate_repo)


def factory_get_exchange_rate_interactor(
    exchange_rate_repo: FromSimpleDi[ExchangeRateRepository],
) -> GetExchangeRateInteractor:
    return GetExchangeRateInteractor(exchange_rate_repo)


def factory_create_exchange_rate_interactor(
    exchange_rate_repo: FromSimpleDi[ExchangeRateRepository],
    currency_repo: FromSimpleDi[CurrencyRepository],
) -> CreateExchangeRateInteractor:
    return CreateExchangeRateInteractor(exchange_rate_repo, currency_repo)


def factory_update_exchange_rate_interactor(
    exchange_rate_repo: FromSimpleDi[ExchangeRateRepository],
    currency_repo: FromSimpleDi[CurrencyRepository],
) -> UpdateExchangeRateInteractor:
    return UpdateExchangeRateInteractor(exchange_rate_repo, currency_repo)


def add_dependencies(container: Container) -> None:
    container.add(
        Connection,
        factory_sqlite_connection,
        deliter_sqlite_connection,
        scope="REQUEST",
    )
    container.add(
        CurrencyRepository,
        factory_sqlite_currency_repo,
        scope="REQUEST",
    )
    container.add(
        ExchangeRateRepository,
        factory_sqlite_exchange_rate_repo,
        scope="REQUEST",
    )

    container.add(
        CreateCurrencyInteracotor,
        factory_create_currency_interactor,
        scope="REQUEST",
    )
    container.add(
        GetCurrenciesInteractor,
        factory_get_currencies_interactor,
        scope="REQUEST",
    )
    container.add(
        GetCurrencyInteractor,
        factory_get_currency_interactor,
        scope="REQUEST",
    )
    container.add(
        ExchangeCurrencyInteractor,
        factory_exchange_interactor,
        scope="REQUEST",
    )
    container.add(
        GetExchangeRatesInteractor,
        factory_get_exchange_rates_interactor,
        scope="REQUEST",
    )
    container.add(
        GetExchangeRateInteractor,
        factory_get_exchange_rate_interactor,
        scope="REQUEST",
    )
    container.add(
        CreateExchangeRateInteractor,
        factory_create_exchange_rate_interactor,
        scope="REQUEST",
    )
    container.add(
        UpdateExchangeRateInteractor,
        factory_update_exchange_rate_interactor,
        scope="REQUEST",
    )
