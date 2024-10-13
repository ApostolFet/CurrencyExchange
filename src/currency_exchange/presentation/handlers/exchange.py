import logging
from dataclasses import asdict
from decimal import Decimal

from currency_exchange.application.interactors.exchange_rates import (
    ExchangeCurrencyInteractor,
)
from currency_exchange.application.models import ExchangeCurrencyDTO
from simple_di.integration import FromSimpleDi, inject
from simple_server import Request, Response, Router

exchange_router = Router("exchange_router")
logger = logging.getLogger(__name__)


@exchange_router.route("GET", "/exchange")
@inject
def exchange_currency(
    request: Request,
    exchange_interactor: FromSimpleDi[ExchangeCurrencyInteractor],
) -> Response:
    logger.info("get exchange rates %s", request)

    base_currency_code = request.query_params.get("from", "")
    target_currency_code = request.query_params.get("to", "")
    amount = request.query_params.get("amount", "1")

    exchange_currency_dto = ExchangeCurrencyDTO(
        base_currency_code, target_currency_code, Decimal(amount)
    )
    exchanged_currence_dto = exchange_interactor(exchange_currency_dto)
    response_body = asdict(exchanged_currence_dto)

    return Response(200, response_body)
