from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    body: dict[str, Any]
    query_params: dict[str, Any]
    path_params: dict[str, Any]


@dataclass
class Response:
    status_code: int = 200
    body: dict[str, Any] | None = None


type Path = str
type Method = str
type Handler = Callable[..., Response]
type HandlerRow = tuple[Method, Path, Handler]
