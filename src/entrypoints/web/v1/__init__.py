from fastapi import APIRouter

from .iam import IamResource
from .users import endpoints as user_endpoints


v1_routers = APIRouter()
endpoints = [user_endpoints]

for endpoint in endpoints:
    endpoint.tags = endpoint.tags.append("v1")
    v1_routers.include_router(endpoint)
