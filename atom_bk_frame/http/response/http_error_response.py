from typing import Callable, Dict, Tuple
from todo_scratch.bk_base.http.request import Request
from todo_scratch.bk_base.http.response.response import Response


class HttpErrorResponse(Response):
    pass


class Response401(HttpErrorResponse):
    default_status = "401"


class Response403(HttpErrorResponse):
    default_status = "403"


class Response404(HttpErrorResponse):
    default_status = "404"


class Response405(HttpErrorResponse):
    default_status = "405"


def get_404_callback() -> Tuple[Callable, Dict]:
    def error_callback(request: Request, **kwargs) -> Response:
        return Response404(body="not found")

    return error_callback, {}


def get_405_callback() -> Tuple[Callable, Dict]:
    def error_callback(request: Request, **kwargs) -> Response:
        return Response405(body="not allow method")

    return error_callback, {}
