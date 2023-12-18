from typing import Callable

from starlette.requests import Request
from starlette.responses import JSONResponse

from src._seedwork.exceptions import CustomException


def http_exception_factory(status_code: int) -> Callable:
    def http_exception(_: Request, exception: CustomException) -> JSONResponse:
        return JSONResponse(
            status_code=status_code, content={"message": exception.message}
        )

    return http_exception
