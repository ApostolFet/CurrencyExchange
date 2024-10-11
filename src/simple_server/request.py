from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    body: dict[str, Any]
    query_params: dict[str, Any]
    path_params: dict[str, Any]
