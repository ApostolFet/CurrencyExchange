from collections.abc import Callable
from typing import Any, Literal

from simple_server.match_path import PathNotMatchError, match_path
from simple_server.request import Request

type Path = str
type Method = str
type Handler = Callable[..., dict[Any, Any]]
type HandlerRow = tuple[Method, Path, Handler]


class RequestNotHandledError(Exception): ...


class Router:
    def __init__(self, name: str) -> None:
        self.name = name
        self._handler_registry: list[HandlerRow] = []

    def route(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE", "PUT"],
        path: str,
    ) -> Callable[[Callable[..., dict[Any, Any]]], None]:
        def decorate_handler(func: Callable[..., dict[Any, Any]]) -> None:
            self._handler_registry.append((method, path, func))

        return decorate_handler

    def handle(self, request: Request, method: str, path: str) -> dict[Any, Any]:
        for registry_method, registry_path, registry_handler in self._handler_registry:
            if registry_method != method:
                continue

            try:
                path_params = match_path(path, registry_path)
            except PathNotMatchError:
                continue
            else:
                request.path_params.update(path_params)

            return registry_handler(request)

        raise RequestNotHandledError
