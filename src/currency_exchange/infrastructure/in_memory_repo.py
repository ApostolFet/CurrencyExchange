from typing import override

from currency_exchange.application.exceptions import (
    CurrencyNotFoundError,
    ExchangeRateNotFoundError,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.domain.models import Currency, ExchangeRate


class InMemoryCurrencyRepository(CurrencyRepository):
    def __init__(self) -> None:
        self._currency_list: list[Currency] = []

    @override
    def get_all(self) -> list[Currency]:
        return self._currency_list

    @override
    def get_by_code(self, code: str) -> Currency:
        filtered_currency = filter(
            lambda currency: currency.code.value == code,
            self._currency_list,
        )

        try:
            currency = next(filtered_currency)
        except StopIteration:
            raise CurrencyNotFoundError(
                f"Currency with code <{code}> was not found"
            ) from None
        return currency

    @override
    def get_pair(self, codes: tuple[str, str]) -> tuple[Currency, Currency]:
        base_currency = self.get_by_code(codes[0])
        target_currency = self.get_by_code(codes[1])
        return base_currency, target_currency

    @override
    def add(self, currency: Currency) -> None:
        self._currency_list.append(currency)


class InMemoryExchangeRateRepository(ExchangeRateRepository):
    def __init__(self) -> None:
        self._exchange_rates: set[ExchangeRate] = set()

    @override
    def get_all(self) -> list[ExchangeRate]:
        return list(self._exchange_rates)

    @override
    def get_by_currency_codes(self, base_code: str, target_code: str) -> ExchangeRate:
        filtered_exchange_rates = filter(
            lambda exchange_rate: exchange_rate.base_currency.code.value == base_code
            and exchange_rate.target_currency.code.value == target_code,
            self._exchange_rates,
        )

        try:
            exchange_rate = next(filtered_exchange_rates)
        except StopIteration:
            raise ExchangeRateNotFoundError(
                f"ExchangeRate with code pair <{base_code}>-<{target_code}>"
                " was not found"
            ) from None
        return exchange_rate

    @override
    def get_related_exchanges_by_currency_codes(
        self, base_code: str, target_code: str, related_code: str
    ) -> tuple[ExchangeRate, ExchangeRate]:
        base_exchange_rate = self.get_by_currency_codes(base_code, related_code)
        target_exchange_rate = self.get_by_currency_codes(related_code, target_code)
        return base_exchange_rate, target_exchange_rate

    @override
    def add(self, exchange_rate: ExchangeRate) -> None:
        self._exchange_rates.add(exchange_rate)
