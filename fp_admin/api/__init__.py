from fastapi import APIRouter

from fp_admin.api.v1 import v1_router
from fp_admin.settings_loader import settings

api_router = APIRouter(prefix=f"{settings.ADMIN_PATH}")
api_router.include_router(v1_router)
