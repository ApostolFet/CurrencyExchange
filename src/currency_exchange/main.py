import logging
import sys

from currency_exchange.presentation.handlers.currencies import currency_router
from currency_exchange.presentation.handlers.exchange import exchange_router
from currency_exchange.presentation.handlers.exchange_rates import exchange_rates_router
from simple_server import SimpleApp


def main() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    server_address = ("0.0.0.0", 8000)
    app = SimpleApp("CurrencyExchange")

    app.include_router(exchange_router)
    app.include_router(currency_router)
    app.include_router(exchange_rates_router)

    app.run(*server_address)


if __name__ == "__main__":
    main()
