# api/__init__.py
from fastapi import APIRouter

from .routes import router as api_router

main_router = APIRouter()
main_router.include_router(api_router, prefix="/api", tags=["api"])