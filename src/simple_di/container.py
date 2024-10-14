from collections.abc import Callable
from typing import Annotated, Any, Final, Literal, get_args, get_origin, get_type_hints

type Scope = Literal["APP", "REQUEST"]
type Getter = Callable[..., object]
type Deliter = Callable[[Any], None]

AVAILIBLE_SCOPES: Final[dict[Scope, list[Scope]]] = {
    "APP": ["APP"],
    "REQUEST": ["REQUEST", "APP"],
}


type FromSimpleDi[T] = Annotated[T, "from_simple_di"]


def mock_deliter(_: object) -> None:
    pass


class Container:
    def __init__(self) -> None:
        self._provides: dict[
            tuple[Scope, type[object]],
            tuple[Getter, Deliter],
        ] = {}
        self._cached_objects: dict[tuple[Scope, type[object]], object] = {}

    def add(
        self,
        provide: type[object],
        getter: Getter,
        deliter: Deliter = mock_deliter,
        scope: Scope = "APP",
    ) -> None:
        self._provides[(scope, provide)] = getter, deliter

    def get(self, provide: type[object], scope: Scope = "APP") -> object:
        active_scope = None
        getter_deliter = None

        for availible_scope in AVAILIBLE_SCOPES[scope]:
            cached_object = self._cached_objects.get((availible_scope, provide), None)
            if cached_object is not None:
                return cached_object

            getter_deliter = self._provides.get((availible_scope, provide))
            if getter_deliter is not None:
                active_scope = availible_scope
                break

        if getter_deliter is None or active_scope is None:
            raise ValueError
        getter, _ = getter_deliter

        inject_keyword = {}
        type_hints = get_type_hints(getter)
        for name, type_ in type_hints.items():
            if get_origin(type_) is not FromSimpleDi:
                continue
            injected_type = get_args(type_)[0]
            inject_keyword[name] = self.get(injected_type, scope=active_scope)
        instance = getter(**inject_keyword)
        self._cached_objects[(active_scope, provide)] = instance
        return instance

    def close(self, scope: Scope = "APP") -> None:
        outdated_objects = []
        for (scope_obj, type_obj), created_object in self._cached_objects.items():
            if scope_obj != scope:
                continue

            getter_deliter = self._provides.get((scope, type_obj))
            if getter_deliter is None:
                raise ValueError

            _, deliter = getter_deliter
            deliter(created_object)

            outdated_objects.append((scope_obj, type_obj))

        for scope_obj, type_obj in outdated_objects:
            del self._cached_objects[(scope_obj, type_obj)]
