from typing import Callable

from starlette.requests import Request
from starlette.responses import JSONResponse

from src._seedwork.exceptions import CustomHTTPException


def http_exception_factory(status_code: int) -> Callable:
    def http_exception(
        request: Request, exception: CustomHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content=exception.content,
            headers=exception.headers,
        )

    return http_exception
