from contextlib import closing
from sqlite3 import Connection
from typing import Any, override
from uuid import UUID

from currency_exchange.application.exceptions import (
    CurrencyNotFoundError,
    ExchangeRateNotFoundError,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.domain.models import Currency, ExchangeRate
from currency_exchange.domain.value_objects import CurrencyCode, Rate


class SQLiteCurrencyRepository(CurrencyRepository):
    def __init__(self, conntection: Connection) -> None:
        self._conn = conntection

    @override
    def get_all(self) -> list[Currency]:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """SELECT id, code, sign, name FROM currencies;"""
            ).fetchall()

        result_currencies: list[Currency] = []
        for row in result:
            id_, code, sign, name = row
            result_currencies.append(
                Currency(
                    name,
                    CurrencyCode(code),
                    sign,
                    UUID(bytes=id_),
                )
            )
        return result_currencies

    @override
    def get_by_code(self, code: str) -> Currency:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                SELECT id, code, sign, name
                FROM currencies
                WHERE code = ?;
                """,
                (code,),
            ).fetchone()

        if not result:
            raise CurrencyNotFoundError(f"Currency with code <{code}> was not found")

        id_, code, sign, name = result
        currency = Currency(
            name,
            CurrencyCode(code),
            sign,
            UUID(bytes=id_),
        )
        return currency

    @override
    def get_pair(self, codes: tuple[str, str]) -> tuple[Currency, Currency]:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                SELECT id, code, sign, name
                FROM currencies
                WHERE code in (?, ?);
                """,
                codes,
            ).fetchmany(2)

        try:
            base_currencies_row = next(filter(lambda row: row[1] == codes[0], result))
        except StopIteration:
            raise CurrencyNotFoundError(
                f"Currency with code <{codes[0]}> was not found"
            ) from None

        try:
            target_currencies_row = next(filter(lambda row: row[1] == codes[1], result))
        except StopIteration:
            raise CurrencyNotFoundError(
                f"Currency with code <{codes[1]}> was not found"
            ) from None

        id_, code, sign, name = base_currencies_row
        base_currencies = Currency(
            name,
            CurrencyCode(code),
            sign,
            UUID(bytes=id_),
        )

        id_, code, sign, name = target_currencies_row
        target_currencies = Currency(
            name,
            CurrencyCode(code),
            sign,
            UUID(bytes=id_),
        )
        return (base_currencies, target_currencies)

    @override
    def add(self, currency: Currency) -> None:
        with self._conn as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                    INSERT INTO currencies (id, code, sign, name)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        code = excluded.code,
                        sign = excluded.sign,
                        name = excluded.name;
                """,
                (
                    currency.id.bytes,
                    currency.code.value,
                    currency.sign,
                    currency.name,
                ),
            )


class SQLiteExchangeRateRepository(ExchangeRateRepository):
    def __init__(self, conntection: Connection) -> None:
        self._conn = conntection

    @override
    def get_all(self) -> list[ExchangeRate]:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                SELECT
                    exchange_rates.id,
                    exchange_rates.rate,
                    base_currency.id,
                    base_currency.code,
                    base_currency.sign,
                    base_currency.name,
                    target_currency.id,
                    target_currency.code,
                    target_currency.sign,
                    target_currency.name
                FROM exchange_rates
                LEFT JOIN currencies as base_currency
                ON exchange_rates.base_currency == base_currency.id
                LEFT JOIN currencies as target_currency
                ON exchange_rates.target_currency == target_currency.id;
                """
            ).fetchall()

        result_exchange_rate: list[ExchangeRate] = []
        for row in result:
            exchange_rate = self._map_row(row)
            result_exchange_rate.append(exchange_rate)
        return result_exchange_rate

    @override
    def get_by_currency_codes(self, base_code: str, target_code: str) -> ExchangeRate:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                SELECT
                    exchange_rates.id,
                    exchange_rates.rate,
                    base_currency.id,
                    base_currency.code,
                    base_currency.sign,
                    base_currency.name,
                    target_currency.id,
                    target_currency.code,
                    target_currency.sign,
                    target_currency.name
                FROM exchange_rates
                LEFT JOIN currencies as base_currency
                ON exchange_rates.base_currency == base_currency.id
                LEFT JOIN currencies as target_currency
                ON exchange_rates.target_currency == target_currency.id
                WHERE base_currency.code = ? AND target_currency.code = ?
                """,
                (base_code, target_code),
            ).fetchone()
        return self._map_row(result)

    @override
    def get_related_exchanges_by_currency_codes(
        self, base_code: str, target_code: str, related_code: str
    ) -> tuple[ExchangeRate, ExchangeRate]:
        with self._conn as conn, closing(conn.cursor()) as cur:
            result = cur.execute(
                """
                SELECT
                    exchange_rates.id,
                    exchange_rates.rate,
                    base_currency.id,
                    base_currency.code,
                    base_currency.sign,
                    base_currency.name,
                    target_currency.id,
                    target_currency.code,
                    target_currency.sign,
                    target_currency.name
                FROM exchange_rates
                LEFT JOIN currencies as base_currency
                ON exchange_rates.base_currency == base_currency.id
                LEFT JOIN currencies as target_currency
                ON exchange_rates.target_currency == target_currency.id
                WHERE
                    base_currency.code = ? AND target_currency.code = ?
                    OR base_currency.code = ? AND target_currency.code = ?
                """,
                (base_code, related_code, related_code, target_code),
            ).fetchmany(2)

        base_exchange_rate = None
        target_exchange_rate = None

        for row in result:
            exchange_rate = self._map_row(row)
            if exchange_rate.base_currency.code.value == base_code:
                base_exchange_rate = exchange_rate
            elif exchange_rate.target_currency.code.value == target_code:
                target_exchange_rate = exchange_rate

        if base_exchange_rate is None:
            raise ExchangeRateNotFoundError(
                f"ExchangeRate with code pair <{base_code}>-<{related_code}>"
                " was not found"
            )

        if target_exchange_rate is None:
            raise ExchangeRateNotFoundError(
                f"ExchangeRate with code pair <{related_code}>-<{target_code}>"
                " was not found"
            )

        return (base_exchange_rate, target_exchange_rate)

    @override
    def add(self, exchange_rate: ExchangeRate) -> None:
        with self._conn as conn, closing(conn.cursor()) as cur:
            cur.execute(
                """
                    INSERT INTO exchange_rates (id,base_currency,target_currency,rate)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        base_currency = excluded.base_currency,
                        target_currency = excluded.target_currency,
                        rate = excluded.rate;
                """,
                (
                    exchange_rate.id.bytes,
                    exchange_rate.base_currency.id.bytes,
                    exchange_rate.target_currency.id.bytes,
                    exchange_rate.rate.value,
                ),
            )

    def _map_row(self, row: Any) -> ExchangeRate:
        (
            exchange_rates_id,
            exchange_rates_rate,
            base_currency_id,
            base_currency_code,
            base_currency_sign,
            base_currency_name,
            target_currency_id,
            target_currency_code,
            target_currency_sign,
            target_currency_name,
        ) = row

        base_currency = Currency(
            id=UUID(bytes=base_currency_id),
            code=CurrencyCode(base_currency_code),
            name=base_currency_name,
            sign=base_currency_sign,
        )

        target_currency = Currency(
            id=UUID(bytes=target_currency_id),
            code=CurrencyCode(target_currency_code),
            name=target_currency_name,
            sign=target_currency_sign,
        )

        return ExchangeRate(
            id=UUID(bytes=exchange_rates_id),
            rate=Rate(exchange_rates_rate),
            base_currency=base_currency,
            target_currency=target_currency,
        )
