from typing import Callable, Dict, Type

from fastapi.exceptions import RequestValidationError

from src._seedwork.exceptions import (
    AuthenticationException,
    BadRequestException,
    NotAuthenticatedException,
    NotFoundException,
)

from .assertion import assertion_error
from .http import http_exception_factory
from .validation import validation_error

# Catalog all exceptions {Calss Type: callable}
exceptions_catalog: Dict[Type, Callable] = {
    AssertionError: assertion_error,
    RequestValidationError: validation_error,
    BadRequestException: http_exception_factory(400),
    NotFoundException: http_exception_factory(404),
    AuthenticationException: http_exception_factory(401),
    NotAuthenticatedException: http_exception_factory(403),
}
