from fastapi import APIRouter
from auth.router import router as auth_router
from users.router import router as users_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])