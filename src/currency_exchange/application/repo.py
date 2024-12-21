from typing import Protocol

from currency_exchange.domain.models import Currency, ExchangeRate


class CurrencyRepository(Protocol):
    def get_all(self) -> list[Currency]: ...

    def get_by_code(self, code: str) -> Currency: ...

    def get_pair(self, codes: tuple[str, str]) -> tuple[Currency, Currency]: ...

    def add(self, currency: Currency) -> None: ...

    def remove(self, currency: Currency) -> None: ...


class ExchangeRateRepository(Protocol):
    def get_all(self) -> list[ExchangeRate]: ...

    def get_by_currency_codes(self, base_code: str, target_code: str) -> ExchangeRate:
        """Raise ExchangeRateNotFoundError"""
        ...

    def get_related_exchanges_by_currency_codes(
        self,
        base_code: str,
        target_code: str,
        related_code: str,
    ) -> tuple[ExchangeRate, ExchangeRate]:
        """Raise ExchangeRateNotFoundError"""
        ...

    def add(self, exchange_rate: ExchangeRate) -> None: ...
