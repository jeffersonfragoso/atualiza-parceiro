from fastapi import APIRouter
from fastapi.responses import JSONResponse



class IamResource:

  endpoints = APIRouter(prefix="/iam", tags=["iam"])

  @endpoints.post("")
  async def sign_in():
    return JSONResponse({"OK": "OK"})

  @endpoints.get("")
  async def sign_up():
    return JSONResponse({"OK": "OK"})

  @endpoints.post("")
  async def current_user():
    return JSONResponse({"OK": "OK"})
