import logging
from typing import Any

from simple_server import Request, Router
from simple_server.types import Response

exchange_rates_router = Router("exchange_rates_router")
logger = logging.getLogger(__name__)


@exchange_rates_router.route("GET", "/exchangeRates")
def get_exchange_rates(request: Request) -> Response:
    logger.info(f"get exchange rates {request}")

    return Response(200, {"status": "OK"})


@exchange_rates_router.route("GET", "/exchangeRate/{pair_code}")
def get_exchange_rate(request: Request) -> Response:
    logger.info(f"get exchange rate {request}")

    return Response(200, {"status": "OK"})


@exchange_rates_router.route("POST", "/exchangeRates")
def create_exchange_rate(request: Request) -> Response:
    logger.info(f"create exchange rate: {request}")

    return Response(200, {"status": "OK"})


@exchange_rates_router.route("PATCH", "/exchangeRate/{pair_code}")
def update_exchange_rate(request: Request) -> Response:
    logger.info(f"update exchange rate: {request}")

    return Response(200, {"status": "OK"})
