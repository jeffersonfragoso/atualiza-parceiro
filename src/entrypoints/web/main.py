from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.entrypoints.web.exception_handlers import exceptions_catalog
from src.entrypoints.web.middlewares.access_logger import RequestAccessLoggerMiddleware
from src.entrypoints.web.middlewares.timer import RequestTimeMiddleware
from src.entrypoints.web.v1 import v1_routers
from src.packages._shared.infra.struct_log import setup_logging

LOG_LEVEL = get_settings().log_level
ENABLE_JSON_LOGS = get_settings().enable_json_logs


def register_exceptions(app: FastAPI):
    for exception_type, _callable in exceptions_catalog.items():
        app.add_exception_handler(exception_type, _callable)


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
        update_request_header=True,
    )
    app.add_middleware(RequestTimeMiddleware)
    app.add_middleware(RequestAccessLoggerMiddleware)


def register_routes(app: FastAPI):
    app.include_router(v1_routers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(LOG_LEVEL, ENABLE_JSON_LOGS)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Atualiza parceiro", description="Atualizaparceiro description", lifespan=lifespan
    )

    register_routes(app)
    register_exceptions(app)
    register_middlewares(app)

    return app
