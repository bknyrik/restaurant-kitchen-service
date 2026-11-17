from urllib.parse import urlencode

from flask import Request


def query_transform(request: Request, **kwargs) -> str:
    query_params = dict(request.args)

    for key, value in kwargs.items():
        if value is not None:
            query_params[key] = value
        else:
            query_params.pop(key, None)

    return f"?{urlencode(query_params)}"
