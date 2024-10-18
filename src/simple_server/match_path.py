from simple_server.exceptions import PathNotMatchError


def match_path(path: str, template: str) -> dict[str, str]:
    """Match the path and template with a possible path parameter

    Raise PathNotMatchError if the path is not matched with the template

    Examples:

    1. Match with path parametr
    >>> match_path("/items/1", "/items/{item_id}")
    {'item_id': '1'}

    2. Match path without path parametr (return empty dict)
    >>> match_path("/items", "/items")
    {}

    3. Not match path
    >>> match_path("/tasks", "/items")
    Traceback (most recent call last):
        ...
    PathNotMatchError


    >>> match_path("/exchangeRate/RUBUSD", "/exchangeRate/{pair_code}")
    {'pair_code': 'RUBUSD'}
    """
    parse_template = template.replace("}", "{").rstrip("{").split("{")
    prefix = parse_template[0]

    if not path.startswith(prefix):
        raise PathNotMatchError

    path_param_index = 1

    if len(parse_template) <= path_param_index:
        if path != prefix:
            raise PathNotMatchError
        return {}

    path_param = parse_template[path_param_index]
    value = path.removeprefix(prefix).rstrip("/")
    if "/" in value:
        raise PathNotMatchError

    return {path_param: value}
