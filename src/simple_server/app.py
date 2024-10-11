import json
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging import getLogger
from socketserver import BaseServer
from typing import Any
from urllib.parse import parse_qsl, urlparse

from simple_server.exceptions import RequestNotHandledError
from simple_server.router import Router
from simple_server.types import Request

logger = getLogger(__name__)


class SimpleApp:
    def __init__(self, name: str):
        self.name = name
        self._routers: list[Router] = []

    def include_router(self, router: Router) -> None:
        self._routers.append(router)

    @property
    def routers(self) -> list[Router]:
        return self._routers

    def run(self, host: str, port: int) -> None:
        httpd = HTTPServer((host, port), handler_factory(self))

        logger.info("START SERVE SERVER ON %s:%s", host, port)
        httpd.serve_forever()


def handler_factory(
    app: SimpleApp,
) -> Callable[[Any, Any, HTTPServer], BaseHTTPRequestHandler]:
    def get_handler(
        request: Any, client_address: Any, server: BaseServer
    ) -> BaseHTTPRequestHandler:
        return RequestHandler(request, client_address, server, app=app)

    return get_handler


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(
        self,
        request: Any,
        client_address: Any,
        server: BaseServer,
        app: SimpleApp,
    ) -> None:
        self._app: SimpleApp = app
        super().__init__(request, client_address, server)

    def do_GET(self) -> None:
        """Serve a GET request."""
        self._handle_request()

    def do_POST(self) -> None:
        """Serve a POST request."""
        self._handle_request()

    def do_PATCH(self) -> None:
        self._handle_request()

    def do_DELETE(self) -> None:
        self._handle_request()

    def _handle_request(self) -> None:
        body = self._parse_body()
        params = self._parse_params()
        path = self._parse_path()
        request = Request(body, params, {})

        for router in self._app.routers:
            try:
                response = router.handle(request, self.command, path)
            except RequestNotHandledError:
                continue
            else:
                if response.body is not None:
                    response_body = json.dumps(response.body)
                    content_type = "application/json"
                else:
                    response_body = ""
                    content_type = "text/plain"

                self.send_response(response.status_code)
                self.send_header("Content-Length", str(len(response_body)))
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(response_body.encode())
                return

        self.send_error(404)

    def _parse_body(self) -> dict[str, Any]:
        content_len = int(self.headers.get("Content-Length", "0"))
        content = self.rfile.read(content_len)
        content_text = content.decode()
        body_type = self.headers.get("Content-Type")

        if body_type == "application/x-www-form-urlencoded":
            body = dict(parse_qsl(content_text))

        elif body_type == "application/json":
            body = json.loads(content_text)
        else:
            body = {}
        return body

    def _parse_params(self) -> dict[str, Any]:
        parse_result = urlparse(self.path)
        params = parse_qsl(parse_result.query)
        return dict(params)

    def _parse_path(self) -> str:
        hierarchical_path = urlparse(self.path).path
        return hierarchical_path
