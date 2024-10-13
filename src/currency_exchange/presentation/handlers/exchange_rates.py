import logging
from dataclasses import asdict
from decimal import Decimal

from currency_exchange.application.interactors.exchange_rates import (
    CreateExchangeRateInteractor,
    GetExchangeRateInteractor,
    GetExchangeRatesInteractor,
    UpdateExchangeRateInteractor,
)
from currency_exchange.application.models import CreateExchangeRateDTO, GetExchangeRate
from simple_di.integration import FromSimpleDi, inject
from simple_server import Request, Router
from simple_server.types import Response

exchange_rates_router = Router("exchange_rates_router")
logger = logging.getLogger(__name__)


@exchange_rates_router.route("GET", "/exchangeRates")
@inject
def get_exchange_rates(
    request: Request,
    get_exchange_rates_interactor: FromSimpleDi[GetExchangeRatesInteractor],
) -> Response:
    logger.info("get exchange rates %s", request)

    exchange_retes = get_exchange_rates_interactor()
    response_body = [asdict(exchange_rate) for exchange_rate in exchange_retes]

    return Response(200, response_body)


@exchange_rates_router.route("GET", "/exchangeRate/{pair_code}")
@inject
def get_exchange_rate(
    request: Request,
    get_exchange_rate_interactor: FromSimpleDi[GetExchangeRateInteractor],
) -> Response:
    logger.info("get exchange rate  %s", request)

    pair_code = request.path_params.get("pair_code", "")
    base_code = pair_code[:3]
    target_code = pair_code[3:]

    get_exchange_rate_dto = GetExchangeRate(base_code, target_code)
    exchange_rete = get_exchange_rate_interactor(get_exchange_rate_dto)

    response_body = asdict(exchange_rete)

    return Response(200, response_body)


@exchange_rates_router.route("POST", "/exchangeRates")
@inject
def create_exchange_rate(
    request: Request,
    create_exchange_rate_interactor: FromSimpleDi[CreateExchangeRateInteractor],
) -> Response:
    logger.info("create exchange rate %s", request)

    base_currency_code = request.body.get("baseCurrencyCode", "")
    target_currency_code = request.body.get("targetCurrencyCode", "")
    rate = request.body.get("rate", "")

    create_exchange_rate_dto = CreateExchangeRateDTO(
        base_currency_code,
        target_currency_code,
        Decimal(rate),
    )
    created_exchange_rate = create_exchange_rate_interactor(create_exchange_rate_dto)
    response_body = asdict(created_exchange_rate)

    return Response(200, response_body)


@exchange_rates_router.route("PATCH", "/exchangeRate/{pair_code}")
@inject
def update_exchange_rate(
    request: Request,
    update_exchange_rate_interactor: FromSimpleDi[UpdateExchangeRateInteractor],
) -> Response:
    logger.info("update exchange rate %s", request)

    pair_code = request.path_params.get("pair_code", "")
    base_code = pair_code[:3]
    target_code = pair_code[3:]
    rate = request.body.get("rate", "")

    update_exchange_rate_dto = CreateExchangeRateDTO(
        base_code,
        target_code,
        Decimal(rate),
    )
    updated_exchange_rate = update_exchange_rate_interactor(update_exchange_rate_dto)
    response_body = asdict(updated_exchange_rate)

    return Response(200, response_body)
