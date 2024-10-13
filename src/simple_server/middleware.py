from typing import Protocol

from simple_server.types import Handler, Request, Response


class Middleware(Protocol):
    def __call__(self, handler: Handler, request: Request) -> Response: ...
