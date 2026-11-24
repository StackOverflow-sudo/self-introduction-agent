from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

from app.routers.conversation import router as conversation_router
from app.routers.product import router as product_router
from app.routers.chat import router as chat_router
from app.routers.chat_thread import router as chat_thread_router

setup_logging()
logger = get_logger(__name__)

from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres import PostgresSaver

from app.agent.graph import build_agent
from app.core.config import settings


from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from app.agent.graph import build_agent
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = ConnectionPool(
        settings.PG_DSN,
        max_size=10,
        kwargs={"autocommit": True, "prepare_threshold": 0},
        open=False,
    )
    pool.open()

    try:
        checkpointer = PostgresSaver(pool)
        checkpointer.setup()
        app.state.agent = build_agent(checkpointer)
        yield
    finally:
        pool.close()


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.include_router(product_router)
app.include_router(conversation_router)


@app.get("/health")
def health() -> dict:
    logger.info("health check")
    return {"status": "ok", "app": settings.APP_NAME}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("未处理异常: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})

app.include_router(chat_router)

app.include_router(chat_thread_router)