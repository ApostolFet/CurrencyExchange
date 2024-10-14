import sqlite3
from decimal import Decimal


def adapt_decimal(value: Decimal) -> str:
    return str(value)


def convert_decimal(value: bytes) -> Decimal:
    return Decimal(value.decode())


def register_decimal() -> None:
    sqlite3.register_adapter(Decimal, adapt_decimal)
    sqlite3.register_converter("decimal", convert_decimal)
