import logging
from typing import Any

from simple_server import Request, Router

exchange_rates_router = Router("exchange_rates_router")
logger = logging.getLogger(__name__)


@exchange_rates_router.route("GET", "/exchangeRates")
def get_exchange_rates(request: Request) -> dict[Any, Any]:
    logger.info(f"get exchange rates {request}")
    return {}


@exchange_rates_router.route("GET", "/exchangeRate/{pair_code}")
def get_exchange_rate(request: Request) -> dict[Any, Any]:
    logger.info(f"get exchange rate {request}")
    return {}


@exchange_rates_router.route("POST", "/exchangeRates")
def create_exchange_rate(request: Request) -> dict[Any, Any]:
    logger.info(f"create exchange rate: {request}")
    return {}


@exchange_rates_router.route("PATCH", "/exchangeRate/{pair_code}")
def update_exchange_rate(request: Request) -> dict[Any, Any]:
    logger.info(f"update exchange rate: {request}")
    return {}
