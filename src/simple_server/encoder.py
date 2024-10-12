import json
from decimal import Decimal
from typing import Any, override
from uuid import UUID


class SimpleEncoder(json.JSONEncoder):
    @override
    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return float(o)

        if isinstance(o, UUID):
            return str(o)

        return super().default(o)
