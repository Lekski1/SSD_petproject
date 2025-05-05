from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import init_db
from routers.csrf import router as csrf_router
from routers.sql_injection import router as sql_router
from routers.ssrf import router as ssrf_router
from routers.xss import router as xss_router
from routers.xxe import router as xxe


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="SSD our api", 
              lifespan=lifespan, 
              root_path="/vulnerable-app", 
              docs_url="/docs", 
              openapi_url="/openapi.json"
        )

app.include_router(sql_router)
app.include_router(xss_router)
app.include_router(ssrf_router)
app.include_router(csrf_router)
app.include_router(xxe)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)