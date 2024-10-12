from currency_exchange.application.exceptions import ExchangeRateNotFoundError
from currency_exchange.application.models import (
    CreateExchangeRateDTO,
    CurrencyDTO,
    ExchangeCurrencyDTO,
    ExchangedCurrencyDTO,
    ExchangeRateDTO,
    GetExchangeRate,
)
from currency_exchange.application.repo import (
    CurrencyRepository,
    ExchangeRateRepository,
)
from currency_exchange.domain.models import ExchangeRate
from currency_exchange.domain.services import (
    exchange_currency,
    merge_exchange_rate,
    reverse_exchange_rate,
)
from currency_exchange.domain.value_objects import Rate


class GetExchangeRatesInteractor:
    def __init__(self, exchange_rate_repo: ExchangeRateRepository):
        self._exchange_rate_repo = exchange_rate_repo

    def __call__(self) -> list[ExchangeRateDTO]:
        exchange_rates = self._exchange_rate_repo.get_all()

        exchange_rates_dto = [
            ExchangeRateDTO.from_domain(exchange_rate)
            for exchange_rate in exchange_rates
        ]
        return exchange_rates_dto


class GetExchangeRateInteractor:
    def __init__(self, exchange_rate_repo: ExchangeRateRepository):
        self._exchange_rate_repo = exchange_rate_repo

    def __call__(
        self,
        get_exchage_rate: GetExchangeRate,
    ) -> ExchangeRateDTO:
        exchange_rate = self._exchange_rate_repo.get_by_currency_codes(
            get_exchage_rate.base_code, get_exchage_rate.target_code
        )
        return ExchangeRateDTO.from_domain(exchange_rate)


class CreateExchangeRateInteractor:
    def __init__(
        self,
        exchange_rate_repo: ExchangeRateRepository,
        currency_repo: CurrencyRepository,
    ):
        self._exchange_rate_repo = exchange_rate_repo
        self._currency_repo = currency_repo

    def __call__(self, exchange_rate_dto: CreateExchangeRateDTO) -> ExchangeRateDTO:
        codes = (
            exchange_rate_dto.base_currency_code,
            exchange_rate_dto.target_currency_code,
        )
        base_currency, target_currency = self._currency_repo.get_pair(codes)

        exchange_rate = ExchangeRate(
            base_currency,
            target_currency,
            Rate(exchange_rate_dto.rate),
        )

        self._exchange_rate_repo.add(exchange_rate)
        return ExchangeRateDTO.from_domain(exchange_rate)


class UpdateExchangeRateInteractor:
    def __init__(
        self,
        exchange_rate_repo: ExchangeRateRepository,
        currency_repo: CurrencyRepository,
    ):
        self._exchange_rate_repo = exchange_rate_repo
        self._currency_repo = currency_repo

    def __call__(self, exchange_rate_dto: CreateExchangeRateDTO) -> ExchangeRateDTO:
        codes = (
            exchange_rate_dto.base_currency_code,
            exchange_rate_dto.target_currency_code,
        )

        exchange_rate = self._exchange_rate_repo.get_by_currency_codes(*codes)
        exchange_rate.rate = Rate(exchange_rate_dto.rate)

        self._exchange_rate_repo.add(exchange_rate)

        return ExchangeRateDTO.from_domain(exchange_rate)


class ExchangeCurrencyInteractor:
    def __init__(
        self,
        exchange_rate_repo: ExchangeRateRepository,
        related_currency_code: str,
    ) -> None:
        self._exchange_rate_repo = exchange_rate_repo
        self._related_currency_code = related_currency_code

    def __call__(
        self,
        exchange_currency_dto: ExchangeCurrencyDTO,
    ) -> ExchangedCurrencyDTO:
        codes = (
            exchange_currency_dto.base_currency_code,
            exchange_currency_dto.target_currency_code,
        )
        try:
            exchange_rate = self._exchange_rate_repo.get_by_currency_codes(*codes)
        except ExchangeRateNotFoundError:
            try:
                reversed_exchange_rate = self._exchange_rate_repo.get_by_currency_codes(
                    codes[1], codes[0]
                )
            except ExchangeRateNotFoundError:
                base_exchange_rate, target_exchange_rate = (
                    self._exchange_rate_repo.get_related_exchanges_by_currency_codes(
                        *codes, self._related_currency_code
                    )
                )
                exchange_rate = merge_exchange_rate(
                    base_exchange_rate, target_exchange_rate
                )

            else:
                exchange_rate = reverse_exchange_rate(reversed_exchange_rate)

        converted_amount = exchange_currency(
            exchange_rate,
            exchange_currency_dto.amount,
        )

        base_currency = CurrencyDTO.from_domain(exchange_rate.base_currency)
        target_currency = CurrencyDTO.from_domain(
            exchange_rate.target_currency,
        )

        return ExchangedCurrencyDTO(
            base_currency,
            target_currency,
            exchange_rate.rate.value,
            exchange_currency_dto.amount,
            converted_amount,
        )
