"""Version 1 endpoint registry."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.api.v1.workouts import router as workouts_router
from app.api.v1.diet import router as diet_router
from app.api.v1.progress import router as progress_router

router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(workouts_router)
router.include_router(diet_router, prefix="/diet", tags=["Diet"])
router.include_router(progress_router, prefix="/progress", tags=["Progress"])
