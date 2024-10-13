from collections.abc import Callable

from simple_server.exceptions import PathNotMatchError, RequestNotHandledError
from simple_server.match_path import match_path
from simple_server.types import Handler, HandlerRow, Method, Path, Request, Response


class Router:
    def __init__(self, name: str) -> None:
        self.name = name
        self._handler_registry: list[HandlerRow] = []

    def route(
        self,
        method: Method,
        path: Path,
    ) -> Callable[[Handler], None]:
        def decorate_handler(func: Handler) -> None:
            self._handler_registry.append((method, path, func))

        return decorate_handler

    def handle(self, request: Request, method: Method, path: Path) -> Response:
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
