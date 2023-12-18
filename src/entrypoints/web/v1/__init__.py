from fastapi import APIRouter

from .health import endpoints as health_endpoints
from .users import endpoints as user_endpoints

v1_routers = APIRouter(prefix="/v1", tags=["v1"])
endpoints = [health_endpoints, user_endpoints]

for endpoint in endpoints:
    v1_routers.include_router(endpoint)
