from fastapi import APIRouter
from auth.router import router as auth_router
from users.router import router as users_router
from students.router import router as students_router
from groups.router import router as groups_router

router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(students_router, prefix="/students", tags=["Student Profiles"])
router.include_router(groups_router, prefix="/groups", tags=["Groups"])