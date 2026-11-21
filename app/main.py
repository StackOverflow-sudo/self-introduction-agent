from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")


@app.get("/health")
def health() -> dict:
    logger.info("health check")
    return {"status": "ok", "app": settings.APP_NAME}

from app.routers.product import router as product_router

app.include_router(product_router)