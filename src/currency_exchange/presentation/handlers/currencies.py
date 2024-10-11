import logging
from typing import Any

from simple_server import Request, Router

currency_router = Router("currency_router")
logger = logging.getLogger(__name__)


@currency_router.route("GET", "/currencies")
def get_currencies(request: Request) -> dict[Any, Any]:
    logger.info(f"get currencies {request}")
    return {}


@currency_router.route("GET", "/currency/{code}")
def get_currency(request: Request) -> dict[Any, Any]:
    logger.info(f"get currency {request}")
    return {}


@currency_router.route("POST", "/currencies")
def create_currency(request: Request) -> dict[Any, Any]:
    logger.info("create currency")
    return {}
