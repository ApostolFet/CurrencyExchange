import logging
from dataclasses import asdict

from currency_exchange.application.exceptions import (
    CurrencyCodeAlreadyExistsError,
    CurrencyNotFoundError,
)
from currency_exchange.application.interactors.currencies import (
    CreateCurrencyInteracotor,
    DeleteCurrencyInteractor,
    GetCurrenciesInteractor,
    GetCurrencyInteractor,
)
from currency_exchange.application.models import CreateCurrency
from simple_di.integration import FromSimpleDi, inject
from simple_server import Request, Router
from simple_server.types import Response

currency_router = Router("currency_router")
logger = logging.getLogger(__name__)


@currency_router.route("GET", "/currencies")
@inject
def get_currencies(
    request: Request, get_currencies_interactor: FromSimpleDi[GetCurrenciesInteractor]
) -> Response:
    logger.info("get currencies %s", request)

    currencies = get_currencies_interactor()
    response_body = [asdict(currency) for currency in currencies]
    return Response(200, response_body)


@currency_router.route("GET", "/currency/{code}")
@inject
def get_currency(
    request: Request,
    get_currency_interactor: FromSimpleDi[GetCurrencyInteractor],
) -> Response:
    logger.info("get currency %s", request)

    code = request.path_params.get("code", "")

    try:
        currency = get_currency_interactor(code)
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except CurrencyNotFoundError as ex:
        return Response(404, {"message": str(ex)})

    response_body = asdict(currency)
    return Response(200, response_body)


@currency_router.route("POST", "/currencies")
@inject
def create_currency(
    request: Request,
    create_currency_interactor: FromSimpleDi[CreateCurrencyInteracotor],
) -> Response:
    logger.info("create currency %s", request)

    name = request.body.get("name")
    code = request.body.get("code")
    sign = request.body.get("sign")

    if name is None or code is None or sign is None:
        empty_fields = "; ".join(
            (
                field_name
                for field_name, value in (
                    ("name", name),
                    ("code", code),
                    ("sign", sign),
                )
                if value is None
            )
        )
        return Response(
            400,
            {"message": f"Fields <{empty_fields}> not filled in"},
        )

    create_currency = CreateCurrency(name, code, sign)
    try:
        created_currency = create_currency_interactor(create_currency)
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except CurrencyCodeAlreadyExistsError as ex:
        return Response(409, {"message": str(ex)})

    response_body = asdict(created_currency)

    return Response(201, response_body)


@currency_router.route("DELETE", "/currency/{code}")
@inject
def delete_currency(
    request: Request,
    delete_currency_interactor: FromSimpleDi[DeleteCurrencyInteractor],
) -> Response:
    logger.info("delete currency %s", request)

    code = request.path_params.get("code", "")

    try:
        delete_currency_interactor(code)
    except ValueError as ex:
        return Response(400, {"message": str(ex)})
    except CurrencyNotFoundError as ex:
        return Response(404, {"message": str(ex)})

    return Response(200)
