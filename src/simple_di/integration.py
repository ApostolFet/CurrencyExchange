__all__ = ["FromSimpleDi"]

from collections.abc import Callable
from functools import wraps
from typing import (
    Concatenate,
    ParamSpec,
    get_args,
    get_origin,
    get_type_hints,
    override,
)

from simple_di.container import Container, FromSimpleDi
from simple_server.app import SimpleApp
from simple_server.middleware import Middleware
from simple_server.types import Handler, Request, Response

Params = ParamSpec("Params")


def inject(
    handler: Callable[Concatenate[Request, Params], Response],
) -> Callable[[Request], Response]:
    @wraps(handler)
    def wraper(
        request: Request, *args: Params.args, **kwargs: Params.kwargs
    ) -> Response:
        container: Container | None = request.context.pop("simple_container")
        if container is None:
            return handler(request, *args, **kwargs)

        type_hints = get_type_hints(handler)
        for name, type_ in type_hints.items():
            if get_origin(type_) is not FromSimpleDi:
                continue
            injected_type = get_args(type_)[0]
            kwargs[name] = container.get(injected_type, scope="REQUEST")

        try:
            result = handler(request, *args, **kwargs)
        finally:
            container.close(scope="REQUEST")
        return result

    return wraper


class DiMiddleware(Middleware):
    def __init__(self, container: Container):
        self._container = container

    @override
    def __call__(
        self,
        handler: Handler,
        request: Request,
    ) -> Response:
        request.context["simple_container"] = self._container
        return handler(request)


def setup(app: SimpleApp, container: Container) -> None:
    app.add_middleware(DiMiddleware(container))
