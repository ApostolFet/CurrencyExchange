from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

type ResponseBody = dict[str, Any] | list[dict[str, Any]]


@dataclass
class Request:
    body: dict[str, Any]
    query_params: dict[str, Any]
    path_params: dict[str, Any]
    context: dict[str, Any]


@dataclass
class Response:
    status_code: int = 200
    body: ResponseBody | None = None


type Path = str
type Method = str
type Handler = Callable[[Request], Response]
type HandlerRow = tuple[Method, Path, Handler]
