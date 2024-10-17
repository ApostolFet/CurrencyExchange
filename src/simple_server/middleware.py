from typing import Protocol, override

from simple_server.types import Handler, Request, Response


class Middleware(Protocol):
    def __call__(self, handler: Handler, request: Request) -> Response: ...


class CORSMiddleware(Middleware):
    def __init__(
        self,
        *,
        allow_origins: list[str],
        allow_methods: list[str],
        allow_headers: list[str],
        allow_credentials: bool,
    ):
        self._allow_origins = ", ".join(allow_origins)
        self._allow_methods = ", ".join(allow_methods)
        self._allow_headers = ", ".join(allow_headers)
        self._allow_credentials = allow_credentials

    @override
    def __call__(self, handler: Handler, request: Request) -> Response:
        response = handler(request)
        response.headers["Access-Control-Allow-Origin"] = self._allow_origins
        response.headers["Access-Control-Allow-Methods"] = self._allow_methods
        response.headers["Access-Control-Allow-Headers"] = self._allow_headers
        if self._allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response
