from sqlite3 import Connection, connect


def up() -> None:
    db_path = "currency_exchange.db"
    connection = connect(db_path)
    try:
        upgrade(connection)
    finally:
        connection.close()


def down() -> None:
    db_path = "currency_exchange.db"
    connection = connect(db_path)
    try:
        downgrade(connection)
    finally:
        connection.close()


def upgrade(connection: Connection) -> None:
    with connection as conn:
        conn.executescript(
            """
        CREATE TABLE IF NOT EXISTS currencies (
            id BLOB(16) PRIMARY KEY,
            code TEXT UNIQUE CHECK(length(code) <= 3),
            sign TEXT CHECK(length(code) <= 5),
            name TEXT CHECK(length(code) <= 30)
        );

        CREATE TABLE IF NOT EXISTS exchange_rates (
            id BLOB(16) PRIMARY KEY,
            base_currency BLOB(16) REFERENCES currencies(id) ON DELETE CASCADE,
            target_currency BLOB(16) REFERENCES currencies(id) ON DELETE CASCADE,
            rate DECIMAL(16, 6)
        );

        CREATE INDEX IF NOT EXISTS exchange_rates_base_currency
        ON exchange_rates(base_currency);

        CREATE INDEX IF NOT EXISTS exchange_rates_target_currency
        ON exchange_rates(target_currency);

        CREATE UNIQUE INDEX IF NOT EXISTS exchange_rates_currencies
        ON exchange_rates(base_currency, target_currency);
        """,
        )


def downgrade(connection: Connection) -> None:
    with connection as conn:
        conn.executescript(
            """
        DROP INDEX IF EXISTS exchange_rates_target_currency;
        DROP INDEX IF EXISTS exchange_rates_base_currency;

        DROP TABLE IF EXISTS exchange_rates;
        DROP TABLE IF EXISTS currencies;
        """,
        )
