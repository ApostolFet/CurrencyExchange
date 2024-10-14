import sqlite3
from collections.abc import Iterator
from sqlite3 import Connection, connect

import pytest

from currency_exchange.infrastructure.database.converters import register_decimal
from currency_exchange.infrastructure.database.migrations import (
    create_tables_currency_exchange,
)


@pytest.fixture
def connection_in_memory_db() -> Iterator[Connection]:
    register_decimal()
    connection = connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

    create_tables_currency_exchange.upgrade(connection)
    try:
        yield connection
    finally:
        connection.close()
