from currency_exchange.application.models import (
    CreateCurrency,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
)
from currency_exchange.domain.models import Currency
from currency_exchange.domain.value_objects import CurrencyCode


class GetCurrenciesInteractor:
    def __init__(self, currency_repo: CurrencyRepository):
        self._currency_repo = currency_repo

    def __call__(self) -> list[Currency]:
        return self._currency_repo.get_all()


class GetCurrencyInteractor:
    def __init__(self, currency_repo: CurrencyRepository):
        self._currency_repo = currency_repo

    def __call__(self, code: str) -> Currency:
        return self._currency_repo.get_by_code(code)


class CreateCurrencyInteracotor:
    def __init__(self, currency_repo: CurrencyRepository) -> None:
        self._currency_repo = currency_repo

    def __call__(self, create_currency: CreateCurrency) -> Currency:
        currency = Currency(
            create_currency.name,
            CurrencyCode(create_currency.code),
            sign=create_currency.sign,
        )
        return self._currency_repo.add(currency)
