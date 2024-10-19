import logging
from dataclasses import asdict
from decimal import Decimal, InvalidOperation

from currency_exchange.application.exceptions import ExchangeRateNotFoundError
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

    base_currency_code = request.query_params.get("from")
    target_currency_code = request.query_params.get("to")
    amount = request.query_params.get("amount")

    if base_currency_code is None or target_currency_code is None or amount is None:
        empty_fields = "; ".join(
            (
                field_name
                for field_name, value in (
                    ("from", base_currency_code),
                    ("to", target_currency_code),
                    ("amount", amount),
                )
                if value is None
            )
        )
        return Response(
            400,
            {"message": f"Fields <{empty_fields}> not filled in query"},
        )

    try:
        amount = Decimal(str(amount))
    except InvalidOperation:
        return Response(
            400, {"message": f"Amount must be convertable to decimal, got <{amount}>"}
        )

    exchange_currency_dto = ExchangeCurrencyDTO(
        base_currency_code, target_currency_code, Decimal(str(amount))
    )

    try:
        exchanged_currence_dto = exchange_interactor(exchange_currency_dto)
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except ExchangeRateNotFoundError:
        return Response(
            400,
            {
                "message": "Can't exchange"
                f"from {base_currency_code} to {target_currency_code}"
            },
        )

    response_body = asdict(exchanged_currence_dto)
    return Response(200, response_body)
