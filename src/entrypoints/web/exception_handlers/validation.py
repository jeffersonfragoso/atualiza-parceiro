from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


def validation_error(
    _: Request, exception: RequestValidationError
) -> JSONResponse:
    errors = [
        {
            "localização": pydantic_error["loc"],
            "tipo": pydantic_error["type"],
            "mensagem": pydantic_error["msg"],
        }
        for pydantic_error in exception.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"errors": errors}),
    )
