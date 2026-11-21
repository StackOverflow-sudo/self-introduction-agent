from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.routers.conversation import router as conversation_router
from app.routers.product import router as product_router

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

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