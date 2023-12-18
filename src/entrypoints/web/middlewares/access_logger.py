import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from uvicorn.protocols.utils import get_path_with_query_string

access_logger = structlog.stdlib.get_logger("api.access")


class RequestAccessLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        event_msg = f"Adicionando informações através do Middleware {type(self).__name__}"

        access_logger.info(
            event_msg,
            http={
                "url": get_path_with_query_string(request.scope),
                "method": request.method,
                "status_code": response.status_code,
                "request_id": response.headers["X-Request-ID"],
            },
            network={"client": {"ip": request.client.host, "port": request.client.port}},
            duration=response.headers["X-Process-Time"],
        )

        return response
