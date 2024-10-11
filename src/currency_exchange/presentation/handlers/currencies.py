import logging

from simple_server import Request, Router
from simple_server.types import Response

currency_router = Router("currency_router")
logger = logging.getLogger(__name__)


@currency_router.route("GET", "/currencies")
def get_currencies(request: Request) -> Response:
    logger.info(f"get currencies {request}")
    return Response(200, {"status": "OK"})


@currency_router.route("GET", "/currency/{code}")
def get_currency(request: Request) -> Response:
    logger.info(f"get currency {request}")
    return Response(200, {"status": "OK"})


@currency_router.route("POST", "/currencies")
def create_currency(request: Request) -> Response:
    logger.info(f"create currency {request}")
    return Response(200, {"status": "OK"})
