from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.entrypoints.web.exception_handlers import exceptions_catalog
from src.entrypoints.web.middlewares.timer import RequestTimeMiddleware
from src.entrypoints.web.v1 import v1_routers


def register_exceptions(app: FastAPI):
  for exception_type, _callable in exceptions_catalog.items():
    app.add_exception_handler(exception_type, _callable)


def register_middlewares(app: FastAPI):
  app.add_middleware(RequestTimeMiddleware)


def register_routes(app: FastAPI):
    app.include_router(v1_routers)
    # app.include_router(v2_routers)

    @app.get("/health")
    def _health_check():
      return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)


def create_app() -> FastAPI:
  app = FastAPI(
    title="Atualiza parceiro",
    description="Atualizaparceiro description"
  )

  register_routes(app)
  register_exceptions(app)
  register_middlewares(app)

  return app
