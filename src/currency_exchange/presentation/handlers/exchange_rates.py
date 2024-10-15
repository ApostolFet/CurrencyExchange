import logging
from dataclasses import asdict
from decimal import Decimal, InvalidOperation

from currency_exchange.application.exceptions import (
    ExchangeRateAlreadyExistsError,
    ExchangeRateNotFoundError,
)
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
    try:
        exchange_rete = get_exchange_rate_interactor(get_exchange_rate_dto)
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except ExchangeRateNotFoundError as ex:
        return Response(404, {"message": str(ex)})

    response_body = asdict(exchange_rete)

    return Response(200, response_body)


@exchange_rates_router.route("POST", "/exchangeRates")
@inject
def create_exchange_rate(
    request: Request,
    create_exchange_rate_interactor: FromSimpleDi[CreateExchangeRateInteractor],
) -> Response:
    logger.info("create exchange rate %s", request)

    base_currency_code = request.body.get("baseCurrencyCode")
    target_currency_code = request.body.get("targetCurrencyCode")
    rate = request.body.get("rate")

    if base_currency_code is None or target_currency_code is None or rate is None:
        empty_fields = ";  ".join(
            (
                field_name
                for field_name, value in (
                    ("baseCurrencyCode", base_currency_code),
                    ("targetCurrencyCode", target_currency_code),
                    ("rate", rate),
                )
                if value is None
            )
        )
        return Response(
            400,
            {"message": f"Fields <{empty_fields}> not filled in"},
        )

    try:
        rate_decimal = Decimal(rate)
    except InvalidOperation:
        return Response(
            400, {"message": f"Rate must be convertable to decimal, got <{rate}>"}
        )

    create_exchange_rate_dto = CreateExchangeRateDTO(
        base_currency_code,
        target_currency_code,
        rate_decimal,
    )

    try:
        created_exchange_rate = create_exchange_rate_interactor(
            create_exchange_rate_dto
        )
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except ExchangeRateNotFoundError as ex:
        return Response(404, {"message": str(ex)})
    except ExchangeRateAlreadyExistsError as ex:
        return Response(409, {"message": str(ex)})

    response_body = asdict(created_exchange_rate)

    return Response(200, response_body)


@exchange_rates_router.route("PATCH", "/exchangeRate/{pair_code}")
@inject
def update_exchange_rate(
    request: Request,
    update_exchange_rate_interactor: FromSimpleDi[UpdateExchangeRateInteractor],
) -> Response:
    logger.info("update exchange rate %s", request)

    pair_code = request.path_params.get("pair_code")
    if pair_code is None:
        return Response(400, {"message": "pair code not specified in path params"})

    rate = request.body.get("rate")
    if rate is None:
        return Response(400, {"message": "Fields <rate> not filled in"})

    base_code = pair_code[:3]
    target_code = pair_code[3:]

    try:
        rate_decimal = Decimal(rate)
    except InvalidOperation:
        return Response(
            400, {"message": f"Rate must be convertable to decimal, got <{rate}>"}
        )

    update_exchange_rate_dto = CreateExchangeRateDTO(
        base_code,
        target_code,
        rate_decimal,
    )
    try:
        updated_exchange_rate = update_exchange_rate_interactor(
            update_exchange_rate_dto
        )
    except ExchangeRateNotFoundError as ex:
        return Response(404, {"message": str(ex)})

    response_body = asdict(updated_exchange_rate)
    return Response(200, response_body)
