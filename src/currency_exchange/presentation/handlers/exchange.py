import logging

from simple_server import Request, Response, Router

exchange_router = Router("exchange_router")
logger = logging.getLogger(__name__)


@exchange_router.route("GET", "/exchange")
def get_exchange_rates(request: Request) -> Response:
    logger.info(f"get exchange rates {request}")

    return Response(200, {"status": "OK"})
