from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.entrypoints.web.v1 import v1_routers


app = FastAPI()
app.include_router(v1_routers)

@app.get("/health")
def health_check():
  return JSONResponse({"status": "ok"}, status_code=status.HTTP_200_OK)
