import logging
from typing import Any

from simple_server import Request, Router

exchange_router = Router("exchange_router")
logger = logging.getLogger(__name__)


@exchange_router.route("GET", "/exchange")
def get_exchange_rates(request: Request) -> dict[Any, Any]:
    logger.info(f"get exchange rates {request}")
    return {}
