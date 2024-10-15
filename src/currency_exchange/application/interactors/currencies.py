from currency_exchange.application.models import (
    CreateCurrency,
    CurrencyDTO,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
)
from currency_exchange.domain.models import Currency
from currency_exchange.domain.value_objects import CurrencyCode


class GetCurrenciesInteractor:
    def __init__(self, currency_repo: CurrencyRepository):
        self._currency_repo = currency_repo

    def __call__(self) -> list[CurrencyDTO]:
        currencies = self._currency_repo.get_all()

        currencies_dto = [CurrencyDTO.from_domain(currency) for currency in currencies]

        return currencies_dto


class GetCurrencyInteractor:
    def __init__(self, currency_repo: CurrencyRepository):
        self._currency_repo = currency_repo

    def __call__(self, code: str) -> CurrencyDTO:
        currency_code = CurrencyCode(code)
        currency = self._currency_repo.get_by_code(currency_code.value)

        return CurrencyDTO.from_domain(currency)


class CreateCurrencyInteracotor:
    def __init__(self, currency_repo: CurrencyRepository) -> None:
        self._currency_repo = currency_repo

    def __call__(self, create_currency: CreateCurrency) -> CurrencyDTO:
        currency = Currency(
            create_currency.name,
            CurrencyCode(create_currency.code),
            sign=create_currency.sign,
        )

        self._currency_repo.add(currency)

        return CurrencyDTO.from_domain(currency)
