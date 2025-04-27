from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from database import init_db
from routers.sql_injection import router as sql_router
# from routers.xss import router as xss_router
# from routers.ssrf import router as ssrf_router
# from routers.ddos import router as ddos_router
from routers.xxe import router as xxe

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="SSD our api", lifespan=lifespan)

app.include_router(sql_router)
# app.include_router(xss_router)
# app.include_router(ssrf_router)
# app.include_router(ddos_router)
app.include_router(xxe)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)