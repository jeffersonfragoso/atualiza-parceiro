from fastapi import APIRouter

from .health import endpoints as health_endpoints
from .users import endpoints as user_endpoints

v1_routers = APIRouter(prefix="/v1")

v1_routers.include_router(health_endpoints, prefix="/health", tags=["health"])
v1_routers.include_router(user_endpoints, prefix="/users", tags=["users"])
