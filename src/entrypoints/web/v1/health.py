import structlog
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


log = structlog.stdlib.get_logger()
endpoints = APIRouter(prefix="/health")


@endpoints.get("/")
async def _health_check():
    log.info("Log inicial da requisição")
    return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)
